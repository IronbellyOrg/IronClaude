review: 2 of 3

# Re-review of the revised spec (/sc:spec-panel --mode critique --focus requirements,architecture --re-review)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, sha256 3cd5458f8a2ac3b837384ffb0c2d1ee1a68493aec2a3e3b821f7c0d4938d6464 (referred to as `spec:N`)
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md, sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
- prior: .dev/orca-command-refactor/review/round1.md, sha256 c4362afb78aa75d17cf1450ece503fd82cc170817642c72494b343fd75137946 (`review: 1 of 3`, so N = 2)
- reviewer model used: claude-sonnet-5-5
- evidence available: the three inventories under .dev/orca-command-refactor/inventory/ (`INV-A` = commands-a.md, `INV-B` = commands-b.md). Skill, command and Orca sources named in the spec are not in the sandbox; a claim that rests on them is marked UNVERIFIED.
- read before reviewing: ~/.claude/rules/prompts/document_review_loop_prompts.md (RE-REVIEW prompt, followed in order: roles, Step 1, review number, self-check).
- verification block carried from prior: round1.md M3 and M7 were rejected by the verifier and are notes, not prior blocking findings. They are not re-opened here.

## Step 1, the evidence block (`diff -w BASELINE CANDIDATE`)

Roles: BASELINE = spec-v1.md, CANDIDATE = orca-worker-contract-spec.md, PRIOR = round1.md. The diff has 8 hunks (baseline lines 62, 76, 83, 85, 92, 159, 176, 195-196, 198). Candidate size 58587 bytes, baseline 57763 bytes.

Verbatim `diff -w` output (`<` = BEFORE (baseline), `>` = AFTER (candidate)):

```text
62c62
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
---
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`), or the directory containing the file when that flag takes a file (tdd, init-lite) (M5). Where a command's directory is fixed or generated, its section 3 row names the contract path and the worker reports it in `--report-path` (M5). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
---
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command except `/sc:load` also gains the `## Unattended mode` section (section 2.1); `/sc:load` gets only its usage-line fix (M1, M6). Phase numbers refer to section 6.
83c83
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
---
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract path to `<output>/return-contract.yaml`, the WC-4 path (P1; M2) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
85c85
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
---
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; contract at the fixed `.claude-audit/return-contract.yaml` (M5); output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
---
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` (package id generated, so the worker reports the path; M5) | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome"), at the fixed `.dev/tasks/to-do/return-contract.yaml` since no package exists yet (M5) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
159c159
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
---
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 that section 3 assigns to a phase, except `/sc:load` (M1, M6) (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
176c176
< | AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep -E '^-[^-]'` | prints nothing: edits are additive |
---
> | AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep '^-' \| grep -v '^--- a/'` (M4: also catches deleted `- ` bullet lines) | prints nothing: edits are additive |
195,196c195,196
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
---
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 whose row assigns a phase P1-P3, except `/sc:load` (which has no contract, M6) and the unphased `brainstorm` and `init-lite` (M1), has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `/sc:load` (M6) with `--unattended --output <dir>` | all steps pass |
198c198
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
---
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names the one path `<output>/return-contract.yaml` (M2); workflow states the contract is written for pre-creation STOPs |
```

Self-check (run): every `<` line was found with `grep -cxF` in spec-v1.md and every `>` line in orca-worker-contract-spec.md; no quote was missing, so the roles are not swapped.

## Prior blocking findings

| id | status | basis (AFTER text only) |
|---|---|---|
| M1 | resolved | The defect was AC-1.1 demanding a `## Unattended mode` section on `load`, `brainstorm`, `init-lite`, which their rows exclude (`spec:112`, `spec:84`, `spec:87`). AFTER `spec:195` now restricts AC-1.1 to rows that assign a phase P1-P3, "except `/sc:load` ... and the unphased `brainstorm` and `init-lite` (M1)"; AFTER `spec:76` says the section is added to "every changed command except `/sc:load`". Both unphased commands have small fix "None" (`spec:84`, `spec:87`), so the AC and the rows no longer contradict. Residual wording issues are Medium (F-A, F-B below). |
| M2 | resolved | AFTER `spec:83` fixes adversarial to `<output>/return-contract.yaml`, "the WC-4 path"; AFTER `spec:198` (AC-1.4) names the same single path. Both agree with WC-4 (`spec:62`) and 7.2 step 4 (`spec:183`). No remaining `adversarial/return-contract.yaml` in the candidate (grep of "adversarial/" shows only skill paths). |
| M4 | resolved | AFTER `spec:176` is `grep '^-' \| grep -v '^--- a/'`. Run in the sandbox on a sample diff (`-- removed bullet`, `-----`, `-removed plain`, `-|row`, `--- a/f.md`): all four removed lines print and the file header is excluded. A deleted bullet is now caught. (AC-0.3 at `spec:193` still uses the old regex; see F-C, not blocking because its rows begin with `\|`.) |
| M5 | resolved | AFTER `spec:62` now gives a directory rule for file-valued flags (tdd, init-lite) and says fixed or generated directories are named in the section 3 row. Rows: cleanup-audit `.claude-audit/return-contract.yaml` (`spec:85`); workflow generated `<id>` reported by the worker and the pre-creation STOP at `.dev/tasks/to-do/return-contract.yaml` (`spec:92`); tdd uses the containing directory, so `/sc:tdd ... --output <file>` (AC-2.2, `spec:200`) has a writable location. The wrong outcome (no resolvable contract location for tdd, workflow pre-creation, cleanup-audit) no longer follows. init-lite is a separate Medium (F-A). |
| M6 | resolved | AFTER `spec:195` and `spec:196` (AC-1.2) both exclude `/sc:load`; AFTER `spec:159` and `spec:76` agree. The load row (`spec:112`) and Decisions (`spec:265`) are no longer contradicted. |

## Findings on changed lines

All blocking checks follow the grading sentence of the RE-REVIEW prompt: a finding is blocking only if the stated text, with no further assumption, causes a wrong build. None of the findings below reaches that bar.

No blocking finding is open or new. The findings below are Medium or minor and are listed once, under follow-up candidates.

## Follow-up candidates (Medium and minor; never trigger a revision, never in the Reviser brief)

- **F-A, Medium, origin=changed** (Wiegers, Fowler). `spec:62` now says an `init-lite` contract is written at the directory containing `--output`, but `spec:87` gives init-lite the small fix "None", `spec:195` excludes it from the section requirement, and its report today is `.dev/superclaude/context-audit.md` or `--output` (`INV-A:55`; the inventory verdict is "ready-as-Orca-worker", no unattended mode). Two readings are possible (init-lite writes a contract, or the worker reports the existing report file as `spec:78` says "until Phase 1 adds the contract"). Under the second reading, WC-5 "no report exists" does not apply because the named file exists, so no concrete wrong build follows without a guess. Fix by removing "init-lite" from the WC-4 parenthesis or by assigning it a phase. Same kind of gap: brainstorm and init-lite get no `--unattended` flag (unphased), yet the brief rule at `spec:73` requires `--unattended` in every Task command line (`spec:73` text was not changed; origin of the interaction is the M1 edit).
- **F-B, Medium, origin=changed** (Fowler, Crispin). AC-1.1 (`spec:195`), a P1 check, asserts the section on commands of phases P1-P3, while Phases 2 and 3 edit their own commands later (`spec:160`, `spec:161`) and P1 scope says only that the flag is "accepted by every command ... that section 3 assigns to a phase" (`spec:159`). Whether P1 adds the section to P2 and P3 commands is not stated. If the implementer adds it only in P2/P3, AC-1.1 cannot pass at the end of P1 and "Later phases do not start until the earlier phase's checks ... pass" (`spec:154`). It needs the guess that P1 edits stop at P1 commands, so it is Medium. Same pattern as the already-noted M7 (`round1.md`, rejected), so not re-opened. Fix: scope AC-1.1 to the commands the phase edits.
- **F-C, Medium, origin=unchanged** (Whittaker). AC-0.3 (`spec:193`) keeps `grep -E '^-[^-]'`, the blind spot M4 fixed in AC-C5. It checks HOW-WE-WORK.md routing rows, which begin with `\|`, so the table-row case is caught; a deleted bullet or `---` line in that file would not be. Minor-to-Medium; unchanged line, not quoting a changed line.
- **F-D, Medium, origin=changed** (Nygard, Whittaker). `spec:92` fixes the workflow pre-creation contract at `.dev/tasks/to-do/return-contract.yaml`, one path for every workflow worker in the worktree, while WC-11 (`spec:69`) says two workers in one worktree must never write the same file. Two workflow workers that both stop before a package exists write the same file. `spec:85` accepts the same limit for cleanup-audit and says so ("one audit per worktree at a time (WC-11)"); workflow carries no such note. It needs the assumption of simultaneous pre-creation STOPs, so Medium. Also, `spec:62` for tdd (and the containing-directory rule): two tdd workers with `--output` in the same directory share one `return-contract.yaml`; add the same one-line limit or a slug.
- **F-E, minor, origin=changed** (Crispin). AC-C5 (`spec:176`) now flags every removed line, including a rewritten Usage or argument-hint line. SA-4 (`spec:149`) calls "new flags" additive and names no usage-line exception except load. If an implementer adds `--unattended` by editing an existing usage line, AC-C5 prints it. The wider regex did not create this (the old regex also flagged it); noted only.
- **F-F, minor, origin=unchanged** (Wiegers). SA-4 (`spec:149`) lists named defect fixes but omits cleanup-audit's and index-repo's small fixes (`spec:85`, `spec:86`-index-repo row) from the AC-C5 exemption wording; the AC says "named defect fix" so the reading is inferable.
- **M3, M7**: noted, unactioned (verifier-rejected in `round1.md`); carried unchanged.

Per the Review Loop, the session that ran this review asks the user once per loop whether to open an issue for the Medium and minor findings above and creates none without an answer. This run cannot ask; the coordinator should relay the list.

## What was covered

- Every one of the 8 changed hunks (62, 76, 83, 85, 92, 159, 176, 195-196, 198) was read against the prior blocking findings M1, M2, M4, M5, M6.
- Dependencies of the changed lines read: `spec:60-73` (WC-2 to WC-11), `spec:76-92` (3.1), `spec:94-125` (3.2), `spec:146-149` (SA-1, SA-4), `spec:154-162` (phases), `spec:176`, `spec:182-200` (7.2 and 7.3), `INV-A:35-60` (adversarial, init-lite, brainstorm rows and evidence notes).
- Not covered: whole-document assurance (this is a scoped re-review), line citations into the repository's `src/` tree and Orca sources (not in the sandbox; UNVERIFIED), section 1 evidence and section 9 open decisions (no changed lines).
- coverage: scoped PASS: changed lines + prior blockers

Reviser brief: none (no blocking finding is open).

verdict: PASS
