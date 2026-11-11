review: 2 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md (re-review of round 1)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines; the revised file, edited per `review/revise1.md`)
- candidate SHA-256: `0d68261e01a3ed1635c14612d194b7036278add2ee00b1558b4001bfcd42d22b`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines), SHA-256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the round-1 candidate hash at `.dev/orca-command-refactor/review/round1.md:6`)
- prior: `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`, `verdict: FAIL`), SHA-256 `609f178910416fc82d9f5ddf1c54eaeeb514f28705c1c22764d36db669eacbf8`
- N = 1 + 1 = 2
- reviewer model: claude-haiku-5-5
- focus: requirements, architecture (Whittaker active per `command.md:83`)
- brief: RE-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy, read in full), with the re-review core (roles, Step 1, review number, self-check) applied first
- grading: CRITICAL or MAJOR is blocking only when the grading-check sentence holds with no further assumption; otherwise Medium (follow-up candidate). `origin=changed` means the finding sits on a line the revision changed; `origin=unchanged` means it quotes a changed line that depends on it.

## Coverage

- Read in full: `command.md`, `.dev/orca-command-refactor/README.md`, the RE-REVIEW prompt file, the candidate, the baseline, `review/round1.md`, `review/revise1.md`.
- Inventory and capability citations checked against the files: `inventory/commands-a.md:35,39,55,60,61,66,97`; `inventory/commands-b.md:52,242,272,275`; `inventory/orca-capabilities.md:72-80` (`CAPS:72-80` in spec numbering).
- Step 1 (evidence block) run with `diff -w` below. 13 changed-line pairs, at candidate lines 61, 62, 63, 76, 84, 87, 91, 92, 159, 182, 195, 234 and 245. The line count is 285 in both files, so the numbers match.
- Self-check (role check): each `>` line was grepped with `-F` in the candidate and each `<` line in the baseline. All 13 pairs were found exactly once in their own file. No role was swapped.
- Not checkable in this sandbox: `sk/sc-workflow-protocol/refs/return-contract.md`, `cmd/workflow.md`, `cmd/troubleshoot.md`, `cmd/init-lite.md`, every `src/superclaude/...`, `.dev/codegraph-migration/...` and `.dev/evals/...` path. Any claim that depends on them is marked UNVERIFIED.
- Loop status: this is review 2 of 3. Blocking findings are open, so the verdict is FAIL. One REVISE and one RE-REVIEW (`review: 3 of 3`) remain before escalation.

## Step 1: evidence block

Command run: `diff -w .dev/orca-command-refactor/specs/history/spec-v1.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Lines starting `<` are BEFORE (baseline). Lines starting `>` are AFTER (candidate). Each block is copied verbatim.

BEFORE (baseline), `<` lines:

```text
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | None | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< - (a) **Keep the rule (recommended).** The worker stops, writes the halt to its ledger and contract, and ends `failed`. The person reads the halt and gives the Ruling by running `/sc:implement <plan>` in their own session, which resumes from the ledger.
< - (a) **Only when the user's own instruction to the coordinator names that action for that task (recommended).** The coordinator quotes the instruction in the brief and passes the command's explicit flag; without it every outward default is off (WC-9).
```

AFTER (candidate), `>` lines:

```text
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. An answer may supply only a value the user already gave, quoted in the brief (D4(a)); it never supplies a WC-9 outward flag or an implement Ruling (D2(a)) (R-1). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. Exact paths (R-3): adversarial writes `<output>/adversarial/return-contract.yaml` (`INV-A:35`, `INV-A:60`); workflow gains an `--output <dir>` flag (P1) and writes `<dir>/return-contract.yaml` when it is given, because its package directory `.dev/tasks/to-do/<id>/` is chosen by the command and is not known before dispatch (`INV-B:52`, `INV-B:272`; the package-path contract stays the default, SA-3); troubleshoot gains an output-directory flag (P2), because its default directory `.dev/troubleshoot/<slug>-<timestamp>/` is not known before dispatch (`INV-B:242`). | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome succeeded` only when the contract's `status` is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). Every other case sends `--outcome failed`: `failed`, `blocked`, no report, an empty or missing contract, a `status` outside the four WC-4 values, or a contract that does not parse; the body then says the contract is invalid (R-5). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every command in 3.1 and 3.2 except `load` also gains the `## Unattended mode` section (section 2.1), including a command whose only change is that it accepts the flag (R-4). Phase numbers refer to section 6.
> | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | Accepts `--unattended` as a no-op; section only, no gate or report change (P1, R-4) | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | Accepts `--unattended` as a no-op; section only, no gate or report change (P1, R-4) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Add an output-directory flag so the contract path is known before dispatch (R-3); under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Add the `--output <dir>` contract flag (R-3); write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` (a no-op where a command has no gate) (R-4); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only), brainstorm and init-lite (flag and section only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the `status` in that report under WC-5; its report path is the WC-4 contract path, or in P0 the command's existing report file from §3.1 ("Report today") (R-2).
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming its report file and `~/.claude/WORKER-CONTRACT.md`, that `load` has none, and that no section-4 command has one (R-4) | passes |
> - (a) **Keep the rule (recommended).** The worker stops, writes the halt to its ledger and contract, and ends `failed`. The person reads the halt and gives the Ruling by running `/sc:implement <plan>` in their own session, which resumes from the ledger. Under (a), no coordinator reply, relayed or not, is recorded as a Ruling (R-1; `INV-A:66`).
> - (a) **Only when the user's own instruction to the coordinator names that action for that task (recommended).** The coordinator quotes the instruction in the brief and passes the command's explicit flag; without it every outward default is off (WC-9). An `ask` answer (WC-3) counts only when it quotes the user's own instruction; a coordinator's own "yes" does not (R-1).
```

## Prior blocking findings (round 1)

Regressed: none. Round 1 marked no finding resolved, so no finding can regress.

| Id | Status | Basis |
|---|---|---|
| R-1 | resolved (the defect as stated: a coordinator's own "yes" becoming a flag or a Ruling) | `specs/orca-worker-contract-spec.md:61` (answer limited to user-given values), `:234` (no coordinator reply recorded as a Ruling), `:245` (a coordinator's own "yes" does not count). The new wording conflicts with `:245`: see N-1 |
| R-2 | open | The P0 relaxation changed only step 3 (`:182`). Step 3 still needs an outcome that matches a status, and WC-5 (`:63`) sends `failed` when no contract exists. `:183` (step 4) and `:194` (AC-0.4) still do not define a P0 pass. See R-2 below |
| R-3 | resolved for adversarial, workflow and troubleshoot (`:62`, `:83`, `:91`, `:92`). Residual for `--output <file>` commands (tdd, init-lite) is N-3, Medium | `specs/orca-worker-contract-spec.md:62` (exact-path rule now names three commands), `:83` (`<output>/adversarial/return-contract.yaml`), `:91` (output flag, P2), `:92` (`--output <dir>`, P1); `inventory/commands-a.md:35,60`; `inventory/commands-b.md:52,242,272` |
| R-4 | resolved | `:76` (every 3.1-3.2 command except `load` gains the section), `:84` and `:87` (brainstorm and init-lite rows), `:159` (P1 lists both), `:195` (AC-1.1 matches). The consistency check passes. The init-lite row itself has a new defect, N-2 |
| R-5 | resolved for the stated defect (`status: complete` no longer maps to `succeeded`). Its new consequences are R-2 and N-2 | `specs/orca-worker-contract-spec.md:63` (succeeded only for `succeeded` or `partial`; every other case, including a missing or empty contract, sends `failed`) |

## === REQUIREMENTS ANALYSIS ===

### R-2. The P0 acceptance check cannot pass as written (open)

- Severity: MAJOR. Grade: BLOCKING (an acceptance criterion cannot pass as written). Origin: changed (`:63`, `:182`) on an unchanged dependency (`:183`, `:194`). Experts: Wiegers (testability), Cockburn (acceptance scope), Whittaker (FR-2.1 zero/empty on the P0 path).
- Locations: `specs/orca-worker-contract-spec.md:79` (P0 workers report "the named file until Phase 1 adds the contract"), `:63` (WC-5), `:182` (step 3, changed), `:183` (step 4, unchanged), `:194` (AC-0.4, unchanged). Evidence: `inventory/commands-b.md:242` (troubleshoot writes `return-contract.yaml` only with `--caller task-unified`), so a P0 troubleshoot run has no contract.
- Issue: WC-5 (`:63`) says `--outcome failed` for "an empty or missing contract". A P0 troubleshoot run has none (`:79`; `commands-b.md:242`). Step 3 (`:182`) requires the outcome to "match the status in that report under WC-5". WC-5 defines a status only for a contract, so for `REPORT.md` the step has no value that passes. Step 4 (`:183`) still asserts a WC-4 YAML with `status` and `command`. AC-0.4 (`:194`) says step 4 "uses the command's existing report file" but does not say what that file must contain. The revision fixed the path wording in step 3 and did not fix the outcome rule. The workflow contract also lists `status`, `plan_path` and `reflect_report_path` with no `command` key (`inventory/commands-b.md:272`). Whether the file has `command` is UNVERIFIED (`sk/sc-workflow-protocol/refs/return-contract.md`, outside the sandbox).
- Grading sentence: "An implementer who runs AC-0.4 on `/sc:troubleshoot` in P0 has no contract, so WC-5 (`:63`) sends `--outcome failed`; step 3 (`:182`) then requires that outcome to match 'the status in that report under WC-5', and WC-5 defines no status for a report that is not a contract, so step 3 has no passing value and AC-0.4 (`:194`) cannot pass as written."
- Whittaker attack (FR-2.1, zero/empty contract): the P0 smoke run is the only evidence for the direct route (`:43`). A check that cannot pass gives the phase no gate, so the run either fails and the phase reopens, or the reviser weakens the check silently.
- Recommendation for the reviser (cites R-2): state in WC-5 or AC-0.4 the P0 outcome rule for a Task that has no contract, and give step 4 a P0 pass condition that names the fields the existing report must carry, or defer AC-0.4 step 3 and 4 until P1.

### N-1. WC-3 and D4(a) give opposite results for one ask answer (origin=changed)

- Severity: MAJOR. Grade: BLOCKING (two stated texts contradict each other on the same input). Origin: changed (`:61`, `:245`). Experts: Whittaker (FR-2.3 sentinel: data becomes control), Wiegers (consistency).
- Locations: `specs/orca-worker-contract-spec.md:61` (WC-3, changed): "An answer may supply only a value the user already gave, quoted in the brief (D4(a)); it never supplies a WC-9 outward flag or an implement Ruling (D2(a))." `:245` (D4(a), changed): "An `ask` answer (WC-3) counts only when it quotes the user's own instruction; a coordinator's own "yes" does not (R-1)." `:67` (WC-9, unchanged) and `:208` (AC-4.1, unchanged). Source: `inventory/commands-a.md:66` (the implement rule at `sk/sc-implement-protocol/refs/qa.md:238`).
- Issue: WC-3 limits an answer to values "quoted in the brief" and says it "never supplies a WC-9 outward flag". D4(a) says an `ask` answer that quotes the user's own instruction counts as authorization. The two texts agree that a coordinator's own "yes" is refused. They disagree on an answer that quotes the user's words but not the brief, and on whether that answer may carry a WC-9 flag.
- Grading sentence: "An implementer who follows D4(a) (`:245`) lets a coordinator's `ask` answer that quotes the user's words authorize a WC-9 push, while an implementer who follows WC-3 (`:61`) refuses the same answer, because the words are not quoted in the brief and an answer never supplies a WC-9 flag; the same input gives opposite results, so the worker's push depends on which text is read."
- What works: the coordinator's own "yes" is refused by both texts, so the round-1 defect as stated is closed.
- Recommendation for the reviser (cites N-1): state one rule for an answer that quotes new user words, and make WC-3 and D4(a) say the same thing about it.

### N-2. Init-lite writes no contract, so a successful unattended run is settled as failed (origin=changed)

- Severity: MAJOR. Grade: BLOCKING (an acceptance criterion cannot pass as written; two texts contradict). Origin: changed (`:87` from R-4, `:63` from R-5). Experts: Wiegers (traceability between row and requirement), Nygard (failure path: success reported as failure), Cockburn (acceptance scope).
- Locations: `specs/orca-worker-contract-spec.md:87` (init-lite, changed): "Accepts `--unattended` as a no-op; section only, no gate or report change (P1, R-4)". `:62` (WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml` ... It is written on success, failure, blocked and partial outcomes." `:63` (WC-5, changed): "an empty or missing contract" sends `failed`. `:183` (step 4, `test -s <contract>`). `:196` (AC-1.2, "all steps pass" for each P1 command with `--unattended --output <dir>`). `:159` (P1 lists init-lite). Evidence: `inventory/commands-a.md:55` (init-lite writes no contract today; its report is `.dev/superclaude/context-audit.md`, and the row is "ready-as-Orca-worker").
- Issue: round-1 R-4 suggested "flag accepted, no gate, no change" as one option. The revision took that wording, and it contradicts WC-4 (`:62`). Under the row, init-lite writes no `return-contract.yaml` in unattended mode, so WC-5 (`:63`) sends `failed` for a run that succeeded. AC-1.2 (`:196`) then fails at step 4 (`:183`) for init-lite. The same row also gives `--output <file>` (`:87`), so `<output-dir>` in WC-4 is undefined (N-3).
- Grading sentence: "An implementer who follows the init-lite row (`:87`) writes no `return-contract.yaml` in unattended mode, so WC-5 (`:63`) sends `--outcome failed` for a successful run, and step 4 (`:183`) of AC-1.2 (`:196`) then fails for init-lite, so AC-1.2 cannot pass as written."
- Recommendation for the reviser (cites N-2): either give init-lite a contract row (WC-4 path, which needs a directory and not a file, see N-3), or state in WC-4 that init-lite's contract is excluded and state what WC-5 sends for it. Either way, the row and WC-4 must agree.

## === ARCHITECTURE ANALYSIS ===

No new architecture finding on a changed line. A-1 (partial settles a Task as succeeded, `:63`, `:263`) is carried from round 1 unchanged and still applies, because the revision kept `partial` mapped to `succeeded`. It stays Medium (see follow-ups).

## Guard Condition Boundary Table (guards on changed lines only, per re-review rule 5)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty | empty or missing contract, Task with a contract | failed | `--outcome failed`; body says contract invalid | OK |
| WC-5 outcome mapping | spec:63 | Zero/Empty | P0 troubleshoot, no contract by design (spec:79, commands-b.md:242) | failed | failed; step 3 has no pass value (R-2) | GAP (R-2) |
| WC-5 outcome mapping | spec:63 | Zero/Empty | init-lite, no contract (spec:87, commands-a.md:55) | failed for a successful run | failed (N-2) | GAP (N-2) |
| WC-5 outcome mapping | spec:63 | One/Minimal | `status: partial` | succeeded | succeeded (A-1, carried) | OK (Medium) |
| WC-5 outcome mapping | spec:63 | Typical | `status: succeeded` | succeeded | succeeded | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status: complete` | failed | failed (R-5 fix) | OK |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | workflow status word outside WC-4 (vocabulary UNVERIFIED) | failed | failed; a successful run may be settled failed (N-4) | GAP (N-4, Medium) |
| WC-3 answer source | spec:61 | Legitimate Edge Case | coordinator's own "yes", not quoted from user | not supplied | refused | OK (R-1 fix) |
| WC-3 answer source | spec:61 vs spec:245 | Legitimate Edge Case | ask answer quoting new user words, not in brief | WC-3: not supplied; D4(a): counts | two results | GAP (N-1) |
| WC-3 Ruling guard | spec:61 vs spec:235 | Typical | relayed Ruling under D2(b) | WC-3: never supplied | conflicts with D2(b) | GAP (N-5, Medium) |
| step 3 pass | spec:182 | Zero/Empty | P0 report `REPORT.md`, no WC-4 status | no value to match | undefined | GAP (R-2) |
| WC-4 path | spec:62 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | `<output-dir>` is not a directory | two readings | GAP (N-3, Medium) |
| WC-4 path | spec:62 | Typical | `adversarial --output <dir>` | `<output>/adversarial/return-contract.yaml` | stated | OK (fix needed, commands-a.md:60) |
| WC-4 path | spec:92 | Zero/Empty | workflow in P0, no `--output` | package path `.dev/tasks/to-do/<id>/` | existing contract used | OK (UNVERIFIED fields) |

Input classes left out: Maximum/Overflow for WC-5 (the status is an enumerated string, no capacity bound).

Pipeline Dimensional Analysis: not triggered (no count stage changed; the WC-5 mapping is a classifier).
State Variable Registry: not triggered (`--focus correctness` is not active).

## Follow-up candidates (Medium and minor, not blocking)

No issue was created. This is a loop review, so the list is recorded for the session that ran it to ask the user.

1. N-3 (Medium, origin=changed, quotes `spec:62`): WC-4's `<output-dir>` is "the directory the coordinator passed", but tdd (`spec:90`) and init-lite (`spec:87`) take `--output <file>`. Two readings give two contract paths. Needs a guess, so Medium.
2. N-4 (Medium, origin=changed, quotes `spec:63`): WC-5 now sends `failed` for any status outside the four WC-4 values. The inventory lists workflow's contract fields but not its status values (`inventory/commands-b.md:272`), so a successful workflow run could be settled as failed. UNVERIFIED (`sk/sc-workflow-protocol/refs/return-contract.md:3-19`, outside the sandbox). Before the revision, unknown values sent `succeeded`.
3. N-5 (Medium, origin=changed, quotes `spec:61`): WC-3 says the answer "never supplies ... an implement Ruling (D2(a))" in unconditional form. D2(b) (`spec:235`) would allow a relayed Ruling, and AC-4.1 (`spec:208`) contemplates one. The parenthetical suggests (a) only. State the condition.
4. N-6 (Medium, origin=unchanged, quotes `spec:63`): round-1 R-8 still applies. Contracts are not scheduled for cleanup-audit (`spec:85`), index-repo (`spec:86`), release-split (`spec:89`), tdd (`spec:90`) and troubleshoot (`spec:91`, flag only). WC-4 is generic, so the requirement exists. Under the new WC-5 default, a Task that omits the contract settles `failed` on every unattended run. Stays Medium while WC-4 is read as the scope; it becomes blocking if the phase tables are read as the complete scope.
5. Round-1 items carried and not re-graded in this review: R-6, R-7, R-9, A-1 to A-9. A-1 (`spec:63`, `:263`) still applies, because `partial` still maps to `succeeded`.

UNVERIFIED in this review: the contents of `sk/sc-workflow-protocol/refs/return-contract.md`, `cmd/workflow.md`, `cmd/troubleshoot.md` and `cmd/init-lite.md` (outside the sandbox); whether `/sc:workflow` already has an output-directory flag (`spec:92` assumes it does not, `inventory/commands-b.md:52` does not say); every `src/superclaude/...` path the spec cites.

## Reviser brief

Blocking finding ids: R-2, N-1, N-2.

Restated bullet 6 of the Review Loop: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.

Brief narrowing: none. This brief does not override any clause of the command. Medium and minor findings (N-3 to N-6, R-6 to R-9, A-1 to A-9) are not in the brief and must not be edited.

verdict: FAIL
