review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (round 1)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`)
- baseline: missing (first review; no `--baseline` given)
- prior report: none
- focus: requirements, architecture (panel: Wiegers lead, Adzic, Cockburn; Fowler lead, Newman, Hohpe, Nygard)
- lint: `.dev/orca-command-refactor/review/lint-1.md` (review-lint/1, 0 findings). No lint id to confirm or dismiss.
- reviewer model: claude-haiku-5-5
- line references: `spec:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N; `INV-A:N` = `inventory/commands-a.md` line N; `INV-B:N` = `inventory/commands-b.md` line N; `CAPS:N` = `inventory/orca-capabilities.md` line N.

## Procedure notes

1. **Two first reviews and MERGE: not run.** This session cannot brief a fresh-context second reviewer, so this report is one review. The coordinator must brief a second reviewer with the FIRST-REVIEW brief and merge. A merge keeps every blocking finding (B1-B3), so the FAIL verdict holds whatever a second review adds.
2. **VERIFY: not run.** This brief asks for a review only and requests no revision. A fresh-context VERIFY must confirm B1-B3 before any REVISE.
3. **Lint:** `lint-1.md` reports 0 findings. Nothing to address.
4. **Evidence scope.** The workspace holds only `.dev/orca-command-refactor/`. Citations to `src/superclaude/`, `tests/`, `pyproject.toml`, `CLAUDE.md`, `.dev/codegraph-migration/`, `.dev/evals/` and the installed Orca code are **UNVERIFIED** here. Checkable evidence is the spec and the three inventories. Inventory citations I checked against the inventory text matched, except where M1, m2 and m3 say otherwise.

## Coverage

Read in full: `README.md`, the spec (286 lines), `review/lint-1.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, and the FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (under the sandbox home). Requirements (WC-1 to WC-12, SA-1 to SA-6), the phase plan (section 6), every acceptance check (section 7), and decisions D1 to D5 were checked for internal consistency. Spot-checked spec citations into the inventories: `INV-A:3, :14, :35, :38, :42, :51, :62, :66, :90, :95-96, :106`; `INV-B:3, :31, :47, :49, :52, :65, :105, :109, :122, :242, :272, :294, :301, :311, :320, :323`; `CAPS:34, :49, :52, :73, :79, :80, :88, :90, :92, :97-103, :125-126, :129, :145, :155, :161, :178, :180, :186`.

## Blocking findings

### B1. /sc:load contradicts the contract rule and AC-1.2 (Wiegers, requirements)

- **Issue.** WC-4 requires the command to write `<output-dir>/return-contract.yaml` "on every outcome" (`spec:62`). The load row gives "Report (WC-4): none (see note)" and says load is "not as its own Task" (`spec:112`). Load is also listed in P1 (`spec:159`). AC-1.2 runs the 7.2 live check on every P1 command (`spec:196`), and 7.2 step 4 requires `test -s <contract>` (`spec:183`). AC-1.1 requires every 3.1 and 3.2 command to name `return-contract.yaml` (`spec:195`).
- **Grading sentence.** An implementer who follows the load row builds no contract for `/sc:load`, and then AC-1.2 step 4 fails on load. That is wrong because the acceptance criterion cannot pass as written, and the two requirements contradict each other.
- **Evidence.** `INV-B:31` and `INV-B:62` (load writes no file; context only in chat); `INV-B:65` (use as a brief step, not a Task).
- **Expert.** Wiegers (requirement traceability: WC-4 and the load row cannot both hold).
- **Recommendation.** Either give load a contract, or add an explicit WC-4 exception for load that states its reason and removes it from the AC-1.2 Task list.
- **Priority.** High. P1 cannot close while this stands.

### B2. AC-0.4 step 3 cannot pass in P0 (Adzic, testability)

- **Issue.** AC-0.4 says steps 1-3 and 5-7 pass in P0, with step 4 using the command's existing report (`spec:194`). Step 3 still requires that the `worker_done` report path is the WC-4 contract path and that the outcome matches the contract's status (`spec:182`). For `/sc:troubleshoot`, the report is `REPORT.md` (`spec:91`; `INV-B:242`). The contract arrives only in P1 (`spec:79`), and P0 forbids command edits (`spec:158`).
- **Grading sentence.** An implementer who runs AC-0.4 on `/sc:troubleshoot` in P0 finds that `worker_done`'s report path is `REPORT.md`, not a WC-4 contract path, so step 3 fails. P0 cannot pass without editing the command, which P0 forbids.
- **Evidence.** `spec:182`, `spec:194`, `spec:158`, `INV-B:49` and `INV-B:242`.
- **Expert.** Adzic (testable acceptance criteria).
- **Recommendation.** In P0, step 3 checks the outcome against the command's existing report. The contract-path check applies from P1. Alternatively, drop troubleshoot from AC-0.4.
- **Priority.** High. This is the P0 gate that tests the whole decision.

### B3. The WC-4 contract has no phase for release-split, tdd, troubleshoot or init-lite (Fowler, architecture)

- **Issue.** The 3.1 intro says the ready commands report their named file "until Phase 1 adds the contract" (`spec:79`). P1 (`spec:159`) does not list release-split, tdd, troubleshoot or init-lite. Their rows give no contract: release-split reports `<output>/release-split-report.md` (`spec:89`; `INV-B:122`), tdd reports the TDD file (`spec:90`; `INV-B:222`), troubleshoot reports `REPORT.md` (`spec:91`), and init-lite writes `.dev/superclaude/context-audit.md` with "Small fix: None" (`spec:87`; `INV-A:55`). Their P2 fixes are prompt-gate changes only (`spec:89-91`), and P2's scope names gates only (`spec:160`). AC-2.3 runs 7.2 on each P2 command (`spec:201`), so step 4 (`spec:183`) fails for release-split, tdd and troubleshoot.
- **Grading sentence.** An implementer who follows `spec:79` expects Phase 1 to add the contract to every ready command, then finds that P1 does not list these commands and P2 does not mention a contract, so AC-2.3 step 4 fails for three commands. This needs no assumption beyond the spec's own text.
- **Expert.** Fowler (phase scope against interface).
- **Recommendation.** Assign each 3.1 command's contract to a named phase in its row, and make the `spec:79` intro match.
- **Priority.** High.

## Guard Condition Boundary Table

Triggered: the spec contains outcome mapping, gate resolution and threshold rules (WC-2, WC-4, WC-5, WC-10, 7.2). Guards are enumerated below. Input classes not listed for a guard do not occur for it, as noted.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome mapping | `spec:63` | Zero/Empty | no report file exists | failed branch | `--outcome failed` | OK |
| WC-5 outcome mapping | `spec:63` | One/Minimal | status `partial` | succeeded branch | `--outcome succeeded`; the Task settles and dependents may start (M6) | GAP (M6, Medium) |
| WC-5 outcome mapping | `spec:63` | Typical | status `succeeded` | succeeded branch | `--outcome succeeded` | OK |
| WC-5 outcome mapping | `spec:63` | Sentinel Value Match | status `blocked` | failed branch | `--outcome failed`; `blocked_question` required (`spec:200`) | OK |
| WC-5 outcome mapping | `spec:63` | Legitimate Edge Case | status outside the four-value set (for example `done`), or unparseable YAML | undefined | not specified; 7.2 step 4 (`spec:183`) fails but no outcome is defined | GAP (M16, Medium) |
| WC-4 contract presence | `spec:62` | Zero/Empty | contract absent for a command that has none | n/a | not specified for commands without a contract | GAP (B1, B3) |
| WC-10 wait threshold | `spec:68` | Maximum | one tool call of 240 s, plus 1 s | n/a | limit stated; no outcome defined if exceeded | OK (limit only, not a branch) |
| 7.2 step 2 agentWait | `spec:181` | Zero/Empty | `agentWait` null | pass | pass | OK |
| 7.2 step 2 agentWait | `spec:181` | Sentinel Value Match | `agentWait` set during a legitimate `ask` (WC-3) | fail | the step fails a legitimate wait | GAP (M14, Medium) |
| WC-2 gate resolution | `spec:60` | Legitimate Edge Case | gate with no documented default and no answer flag | (c) blocked | written per section 3 row; some rows name no answer flag | GAP (M4, Medium) |

**Pipeline Dimensional Analysis:** not triggered. The spec describes gates, contracts and phases. It has no multi-stage data flow whose counts change.

## Medium findings (follow-up candidates; not blocking)

Each finding below is Medium because the problem needs an assumption about the reader, or because the spec states a requirement that is simply missing. None fails the review. The coordinator asks the user once whether to open issues for them. No issue is created in this run.

- **M1 (Fowler, Nygard). Evidence contradiction on the direct route.** `spec:23` (E3) cites the return contract with `invocation_method: "skill-direct"` as evidence that Orca workers invoked `/sc:adversarial` and that the work landed as PR #329. `spec:43` says the PR #329 run "proves the nested route, not the direct route", because its brief used an Agent-tool subagent. `INV-A:13` and `INV-A:35` read the same contract as a proven direct route. Both texts cannot describe the same run without a reconciliation. The codegraph files are UNVERIFIED here. Recommendation: state which run each claim refers to.
- **M2 (Nygard). Overstated rule.** `spec:33` (R1) says a command "cannot run as a worker at the current setting" and "would be refused". The same sentence says the enforcing call sites were not traced and are "presumed (UNVERIFIED, `CAPS:103`)". Recommendation: say "presumed refused" and rely on R2 to R5 as the basis.
- **M3 (Newman). Tool parity is asserted, not shown.** `spec:22` (E2) says a worker "has the same tools as a command a person runs". The evidence cites `CAPS:161`, which shows only `--agent claude`. `INV-A:112` lists MCP and Monitor availability in nested subagents as UNVERIFIED. Recommendation: mark tool parity UNVERIFIED, or add a transcript check to AC-0.4.
- **M4 (Wiegers). WC-3 has no answer interface.** `spec:61` requires the command to be re-invoked "with the answer as a flag". Section 3 names answer flags only for some gates (for example cli-eval `--suite`, `spec:104`). For tdd's topic clarification, troubleshoot's `--fix` offer and review-translation's Phase 1 context (`spec:90`, `spec:118`, `spec:117`), no answer flag is named. No acceptance check tests WC-3. Recommendation: name the answer flag per gate, or state that WC-3 is optional for gates without one.
- **M5 (Fowler). AC-C1 and the P0 Orca section may conflict.** AC-C1 (`spec:172`) greps `src/superclaude/core`. P0 adds an Orca section to `HOW-WE-WORK.md` in that tree (`spec:158`). SA-2 (`spec:147`) allows Orca mentions only as an example in the contract file, which is also in that tree. The check passes only if the Orca section avoids the grep token, for example by pointing at `orca-ide skills get orchestration`. Recommendation: say which token pattern the core files may contain, or exempt the routing guide and contract file from AC-C1.
- **M6 (Hohpe). Partial work releases dependents.** WC-5 maps `partial` to `succeeded` (`spec:63`; decision `spec:263`). Orca settles a succeeded Task, and dependents of a failed Task stay blocked (`CAPS:90`), so a succeeded Task releases them (`CAPS:88`, `CAPS:92`: Orca does not start them itself, but the ready view lists them). Section 2.3 orders only report-opening and release (`spec:73`). Nothing says the coordinator must not start dependents on a `partial` report. Recommendation: state that a `partial` contract holds dependents until the coordinator reviews it.
- **M7 (Nygard). No rule for a worker that exits without `worker_done`.** Section 7.2 step 3 waits with `check --wait` in 900 s steps (`spec:182`). Orca says to leave a wait only on positive proof, such as `exited` liveness (`CAPS:126`), and that absence never authorizes retry or release (`CAPS:125`). The spec never states what the coordinator does on `exited` liveness. Recommendation: add an exited-worker branch to section 2.3.
- **M8 (Fowler). Stale install.** WC-4 and section 2.1 depend on `~/.claude/WORKER-CONTRACT.md` (`spec:52`). The spec does not say what an unattended command does when that file is absent, for example after an install that predates P0. Recommendation: fail closed with `status: blocked`, or inline the rules.
- **M9 (Nygard, Hohpe). Parallel edits to product files in one worktree.** WC-11 (`spec:69`) covers only output paths. The 7.2 example uses `--worktree current` (`spec:180`). The P2 and P4 rows for cleanup, improve, task and implement edit product files (`spec:103`, `spec:110`, `spec:121`, `spec:109`). Two parallel code-editing workers in one worktree can overwrite each other's edits, and the spec states no rule against it. Recommendation: require a separate worktree for any worker that edits product files, or order such workers with `--deps`.
- **M10 (Fowler). Standalone behavior change.** SA-3 (`spec:148`) says a standalone run writes the same files it writes today. The workflow fix "write the contract for pre-creation STOPs too" (`spec:92`) is not limited to unattended mode, while WC-4 is scoped to unattended mode (`spec:62`). Recommendation: scope the fix to unattended mode, or record it as a defect fix under SA-4 with its standalone effect stated.
- **M11 (Wiegers, Nygard). Reflect's `--unattended` trigger.** The 3.1 reflect row says `--remediate` should "follow the existing headless auto-accept rule" (`spec:88`). The 3.2 tasklist row uses `--unattended` the same way (`spec:122`). SA-6 (`spec:151`) keys that rule on `claude --print`. The inventory says the headless rule auto-accepts and skips gates (`INV-B:109`). That gives `--unattended` a second trigger and an auto-accept outcome that WC-2 (c) and WC-9 (`spec:60`, `spec:67`) do not reconcile. Recommendation: state exactly what is auto-accepted and whether the brief authorizes it, or resolve remediation to blocked under `--unattended`.
- **M12 (Wiegers). tdd rated ready with a known stall path.** `spec:90` rates tdd ready with a precise prompt. The nested `/task` can still ask the user on ambiguity (`INV-B:219`, citing `sk/task/SKILL.md:49`), and the fix for that is deferred to P2. The spec's rationale for WC-2 (`spec:60`) is that a worker waiting on a prompt is invisible. Recommendation: rate tdd ready only with a named precondition, or test it before P0 closes.
- **M13 (Fowler). auggie-review relies on a flag the command does not show.** `spec:100` says posting "returns only with an explicit `--post-pr`". The row's "Other required change" column says "none". The inventory lists only `--no-post-pr` and `--no-remediation-offer` as off switches (`INV-A:38`). Recommendation: add `--post-pr` to the required-change column, or drop it.
- **M14 (Adzic). Step 2 treats a legitimate `ask` as a failure.** Step 2 requires `agentWait` never to be non-null (`spec:181`). WC-3 makes `ask` a legitimate wait (`spec:61`). Whether `ask` sets `agentWait` is UNVERIFIED (`CAPS:52`, `CAPS:129`: `agentWait` marks a worker parked on a human prompt). Recommendation: state whether an `ask` wait can show `agentWait`, and adjust the pass condition.
- **M15 (Hohpe). Section 6 says phases need no decisions, but D4 governs some P2 flags.** `spec:154` says phases 1 to 3 need no user decision. D4 (`spec:244`) decides whether a brief may authorize `--post-pr` (auggie-review) and task's `commit`/`push` (`spec:121`), and both are P2 rows. Recommendation: state that D4 governs only the brief, not the phase.
- **M16 (Adzic). Unknown or malformed status is undefined.** WC-5 defines outcomes for four status values and a missing report (`spec:63`). Nothing defines the outcome for another value or for unparseable YAML. Recommendation: map every other case to `failed`.

## Minor notes (no action required)

- **m1.** `spec:52` (`install_core.py`), `spec:183` (`pyproject.toml:38`), the `CLAUDE.md` citations, and the `.dev/codegraph-migration` and `.dev/evals` citations (`spec:11`, `spec:22`, `spec:23`, `spec:43`) are UNVERIFIED in this workspace.
- **m2.** `spec:22` says `EVIDENCE.md:45` shows the worker "answered". `CAPS:49` quotes only "state: ready, stage: input_accepted". "Answered" is not in the quote.
- **m3.** `spec:24` cites `CAPS:155` for `nested-worker-depth.js:7-11,18-22`. `CAPS:155` says lines 7-11 and 18-19. The 18-22 range appears at `CAPS:40`.

## Reviser brief

Blocking finding ids: **B1, B2, B3**.

Restated bullet 6 of the Review Loop: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not in this brief and are not to be revised.

verdict: FAIL
