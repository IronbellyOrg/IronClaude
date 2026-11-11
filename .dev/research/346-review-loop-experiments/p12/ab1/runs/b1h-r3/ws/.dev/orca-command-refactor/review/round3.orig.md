review: 3 of 3

# Re-review round 3: orca-worker-contract-spec.md

Command: `/sc:spec-panel`, `--mode critique`, `--focus requirements,architecture`, `--re-review`, `--baseline`.

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 `530bb94dc36fffb71a0dd0f59ecf0aa60e32ab1c485bde6cfedea040d97adda7`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md` sha256 `e28114855e5685eb7f3f2e2652a756ffaac57ed4c9ffb0b7423b91d78a8e8d19` (equals the round-2 candidate hash in `round2.md:8`)
- prior: `.dev/orca-command-refactor/review/round2.md` sha256 `1947503e187795da64d5ae0d360f0c75641f00f2d28f9e1ff688d40ec1a4a08b` (header `review: 2 of 3`, last line `verdict: FAIL`, `round2.md:159`)
- review number: N = 2 + 1 = 3. This is the last review. A blocking finding that stays open escalates to the user; there is no fourth review and no revision (`command.md:261`).
- reviewer model: claude-haiku-5-5 (Haiku 5.5). One reviewer in a fresh context for this run. The VERIFY step was not run in this worker (see Escalation).
- Rules read: `~/.claude/rules/prompts/document_review_loop_prompts.md` was read in full (sandbox `home/.claude/rules/prompts/document_review_loop_prompts.md`), as the hard gate requires.
- Process of the Fix Cycle: `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md` are not in this sandbox. Steps 1-5 were not applied; the rules in `command.md:258-265` stand alone.
- No `--unattended` in the brief, so no worker contract was read or written.
- Evidence: `inventory/` files, `round1.md`, `round2.md`, `spec-v2.md`, the candidate, and `command.md` (the sandbox copy of `/sc:spec-panel`). The README allows only the inventories as checkable evidence. Citations to `command.md` are checkable in the sandbox but are not in the README list, and they are UNVERIFIED against the repo file `src/superclaude/commands/spec-panel.md`, which is not here. Any other citation to `src/`, `plugins/`, `.claude/` or the Orca guides is UNVERIFIED.

Citation convention: `spec:N` = candidate line N. `base:N` = `spec-v2.md` line N. `R1:N` = `round1.md` line N. `R2:N` = `round2.md` line N. `INV-A:N` and `INV-B:N` = inventory lines. `command.md:N` = sandbox `command.md` line N.

## Step 1: evidence block

Roles: BASELINE = `spec-v2.md`, CANDIDATE = `orca-worker-contract-spec.md`, PRIOR = `round2.md`. Output of `diff -w BASELINE CANDIDATE`, copied verbatim. Lines starting `<` are BEFORE (baseline). Lines starting `>` are AFTER (candidate).

```diff
62c62
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`; `verdict` is added when the report states one, for example an audit's PASS or FAIL (M3). It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Exception: `/sc:load` writes no contract (section 3.2 load row; M8). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
---
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`); for a command whose `--output` names a file (tdd, init-lite; R2-2), it is the directory containing that file. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`; `verdict` is added when the report states one, for example an audit's PASS or FAIL (M3). It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Exception: `/sc:load` writes no contract (section 3.2 load row; M8). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
87c87
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
---
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output`; contract `return-contract.yaml` in the directory of `--output` (WC-4; R2-2) | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
90c90
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
---
> | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output`; contract `return-contract.yaml` in the directory of `--output` (WC-4; R2-2) | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
189c189
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
---
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path. In P0, where `troubleshoot` and `adversarial` have no `status` to match, AC-0.4 gives the rule (R2-1).
201c201
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, where step 3's report path is the one the command writes today. Step 4 is replaced for P0, because the contract arrives in P1: `troubleshoot`: `test -s <dir>/REPORT.md`; `workflow`: read `.dev/tasks/to-do/<id>/return-contract.yaml` and assert only that `status` is one of the four values (no `command` key exists, `INV-B:272`); `adversarial`: `test -s` on its existing contract file (the inventory names no field list, `INV-A:35`). Record the results in the phase report; a failure here reopens section 1 (M6) |
---
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, with step 3 replaced for P0 (R2-1): `workflow`, which writes a `status` contract today, passes when `--outcome` matches WC-5 applied to that `status` and its report path is `.dev/tasks/to-do/<id>/return-contract.yaml`; `troubleshoot` and `adversarial` have no `status` field to match (`INV-A:35`), so each passes when `--outcome succeeded` is sent exactly when the file step 4 checks is non-empty, `--outcome failed` otherwise, and its report path is that file. Step 4 is replaced for P0, because the contract arrives in P1: `troubleshoot`: `test -s <dir>/REPORT.md`; `workflow`: read `.dev/tasks/to-do/<id>/return-contract.yaml` and assert only that `status` is one of the four values (no `command` key exists, `INV-B:272`); `adversarial`: `test -s` on its existing contract file (the inventory names no field list, `INV-A:35`). Record the results in the phase report; a failure here reopens section 1 (M6) |
208c208
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
---
> | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic, where `<contract>` is `return-contract.yaml` in the directory of `<file>` (R2-2); `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

Self-check (run before the verdict, `grep -cF`): each of the six AFTER lines occurs once in CANDIDATE, and each of the six BEFORE lines occurs once in BASELINE. The roles hold.

Changed lines: `spec:62`, `spec:87`, `spec:90`, `spec:189`, `spec:201`, `spec:208`. Whitespace-only changes: none.

## Prior blocking findings

Source: the `Reviser brief` in `R2:153` lists R2-1 and R2-2 as blocking. `R2:94-103` lists M3, M4, M6, M7, M8 and M10 as resolved. Under the regressed rule (`command.md:261`), each of those six is checked again below.

| Prior id | Prior status (R2) | Status now | Evidence |
|---|---|---|---|
| R2-1 | blocking | **open** (partial repair) | Workflow and troubleshoot are repaired. The step-3 rule for adversarial (`spec:189`, `spec:201`) takes its file from "its existing contract file", which the spec never names. The adversarial row says "filename not fixed" (`spec:83`), and the inventory records two layouts (`INV-A:35`). The same root cause as M6 below. |
| R2-2 | blocking | **resolved** | `spec:62` adds the file-to-directory rule for tdd and init-lite. `spec:87` and `spec:90` name the contract in the directory of `--output`. `spec:208` (AC-2.2) names the same path. |
| M3 | resolved | resolved (not regressed) | `spec:62` keeps the verdict clause "(M3)". `spec:63` (WC-5) keeps the audit rule unchanged. Residual: F-1. |
| M4 | resolved | resolved (not regressed) | `spec:63` (WC-5) unchanged: missing, empty or unknown `status` maps to failed. `spec:83` unchanged. Residual: F-8. |
| M6 | resolved | **regressed** (blocking) | M6 asked that step 4 be defined "for each P0 command separately" (`R1:39-50`). Step 4 for adversarial at `spec:201` is "`test -s` on its existing contract file", which names no path. `spec:83` says "filename not fixed", and `INV-A:35` records two observed paths: `<output>/adversarial/return-contract.yaml` and `.../adversarial/adversarial/return-contract.yaml`. The check therefore cannot pass as written. |
| M7 | resolved | resolved (not regressed) | AC-C1 at `spec:180-183` is unchanged. Self-test run in this sandbox: the planted sample `orca orchestration worker-start` plus `orca-ide status --json` gives count 2, as `spec:178` says. |
| M8 | resolved | resolved (not regressed) | `/sc:load` exception unchanged at `spec:62`, `spec:76`, `spec:112` and `spec:202`. Residual: F-2. |
| M10 | resolved | resolved (not regressed) | `spec:92` (workflow), `spec:105` (cli-portify), `spec:116` (research), `spec:206` (AC-1.5) and `spec:209` (AC-2.3) unchanged. |

Open blocking findings at this review: R2-1 (open) and M6 (regressed). They share one root cause, the undefined adversarial contract path in P0. One fix closes both.

## New findings on changed lines

### M6 (regressed, BLOCKING; origin=unchanged step 4, depends on changed `spec:201` step 3)

- Quoted: `spec:201`, adversarial step 4: "`adversarial`: `test -s` on its existing contract file (the inventory names no field list, `INV-A:35`)". Step 3 at `spec:189` and `spec:201` uses the same file: "its report path is that file".
- Sentence: An implementer who runs AC-0.4 on `/sc:adversarial --compare <two files> --depth quick --output <dir>` as written must run `test -s` on "its existing contract file". The spec names no path (`spec:83`: "filename not fixed"). The inventory records two layouts (`INV-A:35`). The check tests either the wrong file or no file, so step 4 and the step-3 rule built on it cannot pass as written.
- Note: `spec:83` gives the adversarial row's P1 fix as `<output>/return-contract.yaml`. That is P1, and P0 runs before it (`spec:158`).
- Experts: Crispin (testability), Fowler (interface contract).
- Priority: High. Impact: blocks the P0 gate, which "reopens section 1" on failure (`spec:201`).
- Suggested repair for the user to choose (not a brief, since the review is at 3): (a) name the P0 adversarial path explicitly, for example `<dir>/adversarial/return-contract.yaml` after checking that the output is deterministic; or (b) remove adversarial from P0, which needs only two commands, and test it first in P1, when `spec:83` fixes the path.

### R3-1 (MEDIUM, follow-up; origin=unchanged row, depends on changed `spec:62`)

- Quoted: `spec:120` (spec-panel): "`target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output`; contract".
- Against: `command.md:23` already defines `--output <file>` and `--unattended`. `command.md:460` says "`--output` is file-valued", and `command.md:461` puts the contract at `<report-dir>/return-contract.yaml`.
- The WC-4 carve-out at `spec:62` now covers any file-valued `--output` (directory containing the file), but the row says "add `--output`", a new directory-valued flag. The contract location for spec-panel is therefore undefined, and `--unattended` may be duplicated.
- Why Medium and not blocking: the premise is checked against `command.md`, which is outside the README evidence list. The repo file `src/superclaude/commands/spec-panel.md` is cited at `spec:120` and is not here. This is the same item as round-2 F-6 and round-1 M12, which both graded it Medium.
- Upgrade rule: if the repo `spec-panel.md` matches `command.md:23,455-461`, this becomes blocking under the same reasoning as R2-2.

### R3-2 (MEDIUM, follow-up; origin=changed `spec:87`, `spec:90`, `spec:208`)

- Quoted: `spec:87` and `spec:90` put a contract in the "Report today" column. `spec:79` says "the worker reports the named file until Phase 1 adds the contract". `INV-A:55` says init-lite's report today is `.dev/superclaude/context-audit.md` or `--output`, with no contract.
- Coverage gap: AC-1.5 (`spec:206`) names only workflow and adversarial. AC-2.3 (`spec:209`) names research and cli-portify. AC-2.2 (`spec:208`) checks the tdd contract on the blocked path only. Nothing checks the init-lite contract, and nothing checks the tdd contract on a successful run.
- Priority: Medium. Impact: a new WC-4 path with no acceptance check.

### Minor (origin=changed `spec:201`)

- The outcome rule for troubleshoot and adversarial at `spec:201` takes its outcome from the same `test -s` the coordinator runs. The step-3 match is then true by construction and does not test WC-5 for those two commands. WC-5 says "no report exists" (`spec:63`), while AC-0.4 says "non-empty". This is a naming difference, not a wrong outcome.

## Follow-up candidates (Medium and minor; not blocking)

- **F-1 (Medium, carried).** The `verdict` gate for audits is in WC-5 only (`spec:63`). It is not in §2.3 (`spec:73`), and no AC tests it (`R2:124-129`).
- **F-2 (Medium, carried).** `/sc:load` writes no contract (`spec:62`, `spec:112`), but WC-5 maps "no report exists" to failed (`spec:63`). A load run dispatched as its own Task would always send failed.
- **F-3 (Medium, UNVERIFIED, carried).** AC-0.4 step 4 for workflow asserts four `status` values. `INV-B:272` lists the field names, not their values, so the values are UNVERIFIED.
- **F-4 (minor, carried).** AC-1.5 (`spec:206`) and AC-2.3 (`spec:209`) use parenthetical lists that read as exhaustive.
- **F-5 (minor, carried).** WC-4 (`spec:62`) names both `--output` and `--output-dir`. Every row uses `--output`.
- **F-7 (minor, carried).** `spec:79` says the §3.1 commands are ready today, but `spec:92` requires `--output <dir>` from P1.
- **F-8 (minor, carried).** `spec:83` writes `<output>/return-contract.yaml` and `spec:205` writes `<output-dir>/return-contract.yaml`. Naming drift only.
- **F-9 (minor, carried).** `spec:158` smoke list and `spec:201` name adversarial's flags differently.

Notes carried unchanged from round 1 (verifier rejected): M1, M2, M5, M9, M11, M12. M12 is now partly checkable against `command.md:23,460`; the repo-file check is still needed (R3-1).

## Coverage

Scoped review of the changed lines `spec:62`, `spec:87`, `spec:90`, `spec:189`, `spec:201`, `spec:208`, and of the rows and checks that depend on them: `spec:79`, `spec:83`, `spec:92`, `spec:105`, `spec:112`, `spec:116`, `spec:120`, `spec:158`, `spec:202`, `spec:205`, `spec:206`, `spec:209`. The FR-8 guard check on WC-5 (`spec:63`) is unchanged and has no GAP. Not checked: anything under `src/`, `plugins/`, `.claude/`, or the Orca guides (UNVERIFIED). Live Orca runs were not possible in this sandbox. The `scoped PASS` coverage line does not apply, because the verdict is FAIL (`command.md:259`).

## Escalation (review 3 of 3)

- Open blocking findings: **R2-1 (open)** and **M6 (regressed)**. The Reviser brief is omitted at `review: 3` (`command.md:263`).
- The VERIFY prompt still runs before escalation (`document_review_loop_prompts.md`, "At `review: 3`"). It was not run in this worker, because this worker cannot start a fresh-context verifier. The coordinator must run it on R2-1 and M6, citing `spec:83`, `spec:189`, `spec:201` and `INV-A:35`.
- Question for the user, asked once per loop: open issues for the follow-up candidates F-1 to F-9, R3-1 and R3-2? No issue has been created.
- Decision needed from the user: how to fix the adversarial step in P0 (option (a), name the path, or option (b), move adversarial out of P0). Both options are listed under M6.

verdict: FAIL
