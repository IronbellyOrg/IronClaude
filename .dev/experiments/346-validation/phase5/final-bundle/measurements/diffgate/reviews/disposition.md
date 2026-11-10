# Disposition: spec-panel review 1 of orca-worker-contract-spec.md

Task: task_1e91e91a298a (Task 6, revise the spec). Reviser did not write the review.
Inputs: `.dev/orca-command-refactor/review/spec-panel.md` (13 numbered findings), task list `.dev/orca-command-refactor/review/diffgate-loop/reviser-brief-r1.md` (blocking ids R1.1-R1.7), spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Repo root: /home/coder/workspaces/worktrees/IronClaude/exp346-v-diffgate. `SPEC-OLD:N` = line N of `review/diffgate-loop/doc-r1.md` (byte copy of the spec before this revision). `SPEC:N` = line N of the revised spec.

## Size
`fixcheck --dry-run` printed `bytes_before: 57763`, `bytes_after: 62054` (+4291 bytes, 16 hunks H2.1-H2.16). Line count unchanged (285); every edit is in place on an existing line. Final `fixcheck --dry-run --map review/disposition.md` run: exit 0, `"message": "dry run: fix map would be accepted; nothing written"`, `unmapped: []`, `errors: []`. The binding `fixcheck` (without `--dry-run`) is the coordinator's step.

## Verification of each finding
Each blocking finding's cited sources were re-read in this task (2026-11-08/09), not taken from the review.

| Finding | Verdict | What was read |
|---|---|---|
| R1.1 | Confirmed | `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24` ("`--output` is retired → `E-LEGACY`"; "no yaml on a pre-creation STOP" at :26); `SKILL.md:44` (package id like `TASK-WF-authLogin-20261001-063000`); `refs/return-contract.md:3` (contract inside the generated package), `:39` (pre-creation STOPs: "no package directory, no yaml"); `src/superclaude/commands/tdd.md:49` and `src/superclaude/commands/init-lite.md:32` (`--output` is a file path); `SPEC-OLD:62` (location from `--output` / `--output-dir`), `SPEC-OLD:83` (adversarial at `<output>/adversarial/`). No rule for a missing flag in `SPEC-OLD:62`. |
| R1.2 | Confirmed | `refs/return-contract.md:7` (`status: success \| partial \| failed`); `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:432,436` (`status` nested under top-level `return_contract:`); `src/superclaude/skills/sc-reflect-protocol/SKILL.md:250` (`status: stopped-precondition`); `SPEC-OLD:62` ("keep their fields and add the missing ones" plus a required `status`), `SPEC-OLD:183` (step 4 reads top-level `d['status']`). |
| R1.3 | Confirmed | `SPEC-OLD:64` (command picks "a fresh output directory"), `SPEC-OLD:62,73` (directory fixed in the brief before dispatch), `SPEC-OLD:61` (WC-3 re-invocation in one worker); `.dev/orca-command-refactor/inventory/orca-capabilities.md:116` (`--retry-of` retry of the same Task). |
| R1.4 | Confirmed | `src/superclaude/core/CLAUDE.md:73` (Skill rule fires "When a message starts with `/sc:<name>`"); `SPEC-OLD:65` (WC-7 has no Skill requirement), `SPEC-OLD:184` (step 5 searches only for `AskUserQuestion`), `SPEC-OLD:194` (AC-0.4 checks only the Agent wrapper). |
| R1.5 | Confirmed | `SPEC-OLD:172` (AC-C1 scans `src/superclaude/core` with pattern `orca(-ide)?[[:space:]]+(orchestration\|...)`), `SPEC-OLD:158` (P0 writes `src/superclaude/core/WORKER-CONTRACT.md`), `SPEC-OLD:147` (SA-2 allows Orca as an example inside that file). Text such as `orca orchestration ask` matches the pattern. Corroboration: `origin/master:src/superclaude/core/WORKER-CONTRACT.md:101` holds `orca orchestration check --wait ...` (read with `git show`). |
| R1.6 | Confirmed | `SPEC-OLD:112` (load: "Report: none"), `SPEC-OLD:265` (Decisions: a report for load "would be an unrequested addition"), `SPEC-OLD:195` (AC-1.1 covers every 3.1-3.2 command); `.dev/orca-command-refactor/inventory/commands-b.md:65` (load writes no file). |
| R1.7 | Confirmed | `SPEC-OLD:51` (mode on "when the caller passes `--unattended`", no parse rule), `SPEC-OLD:228` (D1 (a) rests on "a person never types it"), `SPEC-OLD:146,148` (SA-1, SA-3). |
| R1.8 | Not re-verified (minor) | Taken as stated in `review/spec-panel.md:102`; not on the reviser brief. |
| R1.9 | Partly verified (minor) | `ls /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs` failed (no such directory); `origin/master` resolves to `933cf3a4f` here and holds `src/superclaude/core/WORKER-CONTRACT.md`. The 46-command count and `orca_worktree.py:27,53` were not re-read (UNVERIFIED). |
| R1.10-R1.13 | Not re-verified (minor) | Taken as stated in `review/spec-panel.md:104-107`; not on the reviser brief. |

## Disposition table
One row per numbered finding in `review/spec-panel.md:95-107`. Minor findings are rejected for this cycle by rule, not on merit: the reviser brief lists blocking findings only and says "Revise only text a blocking finding names" (`review/diffgate-loop/reviser-brief-r1.md:4,16`), and minor findings "never trigger a revision" (`review/spec-panel.md:110`). Each stays recorded in the review for a later pass.

| # | Finding | Disposition | Where (revised spec) |
|---|---|---|---|
| 1 | R1.1 report location unknowable or undefined | Applied | WC-4 (`SPEC:62`): new `--report-dir <dir>`, separate from each command's own output flags; refusal when missing (no work, no file, WC-5 `failed`); workflow pre-creation STOPs covered. Brief (`SPEC:73`), section 3 "Contract" definition (`SPEC:76`), adversarial row (`SPEC:83`), workflow row (`SPEC:92`, never `--output`), section 7 intro (`SPEC:167`), AC-1.4 (`SPEC:198`), D1 example (`SPEC:228`). |
| 2 | R1.2 `status` collides with existing contract fields | Applied | WC-4 (`SPEC:62`): field renamed `worker_status`; existing contracts and their `status` kept unchanged; mapping `success`→`succeeded`, `partial`→`partial`, gate stop→`blocked`, `failed`/other (e.g. `stopped-precondition`)→`failed`. Consequent renames: WC-2 (`SPEC:60`), WC-5 (`SPEC:63`), 3.2 intro (`SPEC:95`), 7.2 steps 3-4 (`SPEC:182-183`), AC-2.2 (`SPEC:200`), AC-4.1 (`SPEC:208`), Decisions "Status vocabulary" (`SPEC:262`). |
| 3 | R1.3 WC-6 fresh dir vs brief-fixed dir | Applied | WC-6 (`SPEC:64`): coordinator chooses new `--report-dir` (and output location when no resume) in every attempt's brief, retries included; owner column adds the coordinator; a WC-3 re-invocation is the same attempt and replaces its own `blocked` report. Brief (`SPEC:73`), "Fresh dir" meaning (`SPEC:76`). |
| 4 | R1.4 WC-7 lacks the Skill invocation | Applied | WC-7 (`SPEC:65`): worker loads the command's skill with the Skill tool before any other step; reading the file and improvising fails WC-7; cites `src/superclaude/core/CLAUDE.md:73`. Check: 7.2 step 5 (`SPEC:184`) looks for the Skill call; AC-0.4 (`SPEC:194`). |
| 5 | R1.5 AC-C1 scans the contract file | Applied | AC-C1 (`SPEC:172`): `grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:'` added with the reason; SA-2 (`SPEC:147`) states the contract file may name the caller's channels for questions, reports and checks and is excluded from AC-C1. |
| 6 | R1.6 load has no report but AC-1.1 requires one | Applied | AC-1.1 (`SPEC:195`): `/sc:load` exempted by name, citing its 3.2 row and the Decisions table. |
| 7 | R1.7 no parse rule for `--unattended` | Applied | Unattended mode term (`SPEC:51`): only a standalone token outside any quoted argument counts, with the troubleshoot example. D1 (a) (`SPEC:228`): "a person never types it" replaced by a reference to the parse rule. |
| 8 | R1.8 3.1 understates P1 edits (minor) | Rejected | Minor, not on the reviser brief (`reviser-brief-r1.md:6-14`); revising it would change text no blocking finding names (`reviser-brief-r1.md:16`). The review itself says behaviour is inferrable (`spec-panel.md:30`). |
| 9 | R1.9 stale baseline (minor) | Rejected | Minor, not on the reviser brief (`reviser-brief-r1.md:6-14`); the review grades it minor because the claims are true at HEAD `2cb683f5c` and leaves re-baselining to the coordinator (`spec-panel.md:129`). Note for the coordinator: the revised WC-4 and parse rule now agree in substance with `origin/master:src/superclaude/core/WORKER-CONTRACT.md:13,15,32,35` (report directory, `worker_status`, parse rule), except that master also accepts a command's own directory-valued output flag as the report directory. |
| 10 | R1.10 WC-10 covers unsplittable Agent calls (minor) | Rejected | Minor, not on the reviser brief; WC-10 text is not named by any blocking finding (`reviser-brief-r1.md:16`). |
| 11 | R1.11 step 2 cadence vs 900 s step-3 wait (minor) | Rejected | Minor, not on the reviser brief. Step 3 (`SPEC:182`) was edited for R1.2 only; its 900 s timeout was left as is because changing it is not called for by a blocking finding (`reviser-brief-r1.md:16`). |
| 12 | R1.12 transcript tool-call content UNVERIFIED (minor) | Rejected | Minor, not on the reviser brief. Step 5 (`SPEC:184`) now also relies on the transcript for the R1.4 Skill check, so this UNVERIFIED gap now covers that check too; flagged for the coordinator. |
| 13 | R1.13 WC-5 exactly-once vs WC-12 fenced (minor) | Rejected | Minor, not on the reviser brief. WC-5 (`SPEC:63`) was edited for R1.2 only; the fenced exception was not added (`reviser-brief-r1.md:16`). |

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| R1.1 report location | one new `--report-dir` always passed; accept either a command's own directory-valued output flag or `--report-dir` (origin/master's choice) | One flag for every command is the review's recommendation ("one report-directory input the brief always passes, independent of each command's own output flag", `spec-panel.md:95`) and gives one rule instead of a per-command choice. |
| R1.2 field vs file | rename the field (`worker_status`); a separate report file name | A field rename keeps `return-contract.yaml` and every AC that names it (AC-1.1, AC-1.3) unchanged, so fewer hunks; the review offers either (`spec-panel.md:96`). |
| R1.5 exclusion vs forbidding Orca text | exclude the contract file from AC-C1; forbid Orca verbs in it | Exclusion keeps the WC-3/WC-5/WC-12 channel examples the worker needs; forbidding them would need a new statement of where the worker gets the verbs. |
| Minor findings | apply them; reject for this cycle | Brief forbids revising text no blocking finding names (`reviser-brief-r1.md:16`). |
| Placeholder check | grep the revised spec for `TODO`, `TBD`, `FIXME`, `{{`, `placeholder`, `XXX` | Only hit is `cmd/explain.md`'s "TodoWrite" tool name (`SPEC:108`), which is content, not a placeholder. Angle-bracket values such as `<dir>` are parameter names in commands, not unfilled text. |

## Diffgate fixmap
doc_sha: 6c68d0ece899759096d1d8e35226720deeb59e96e771d6f47232364e4a628d17
H2.1 R1.7
H2.2 R1.2,R1.1,R1.3,R1.4
H2.3 R1.1,R1.3
H2.4 R1.1,R1.3
H2.5 R1.1
H2.6 R1.1
H2.7 R1.2
H2.8 R1.5
H2.9 R1.1
H2.10 R1.5
H2.11 R1.2,R1.4
H2.12 R1.4,R1.6
H2.13 R1.1,R1.2
H2.14 R1.2
H2.15 R1.7,R1.1
H2.16 R1.2
