review: 1 of 3

# Merged first review (coordinator; MERGE rule over two independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 7eada379ba2f5c04fc0b109ac220586175ad5801cc64d8d18595a17057f9b2be
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 20d91855bd76c7843b6192c55a1e05220019ae3d881768254eca879299025a39

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M1, M2, M4, M5, M6, M7. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M3 (verifier: The P1 Scope cell states "The WC-4 contract in unattended mode" with no command list, and line 79 says Phase 1 adds the contract to the ready commands. The four commands are therefore covered by that unqualified scope. The failure needs the P1 Commands column to be read as exhaustive for the contract, which is an extra assumption.). The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M1

#### M1.a, from round1-a.md B1: B1. /sc:load contradicts the contract rule and AC-1.2 (Wiegers, requirements)
- **Issue.** WC-4 requires the command to write `<output-dir>/return-contract.yaml` "on every outcome" (`spec:62`). The load row gives "Report (WC-4): none (see note)" and says load is "not as its own Task" (`spec:112`). Load is also listed in P1 (`spec:159`). AC-1.2 runs the 7.2 live check on every P1 command (`spec:196`), and 7.2 step 4 requires `test -s <contract>` (`spec:183`). AC-1.1 requires every 3.1 and 3.2 command to name `return-contract.yaml` (`spec:195`).
- **Grading sentence.** An implementer who follows the load row builds no contract for `/sc:load`, and then AC-1.2 step 4 fails on load. That is wrong because the acceptance criterion cannot pass as written, and the two requirements contradict each other.
- **Evidence.** `INV-B:31` and `INV-B:62` (load writes no file; context only in chat); `INV-B:65` (use as a brief step, not a Task).
- **Expert.** Wiegers (requirement traceability: WC-4 and the load row cannot both hold).
- **Recommendation.** Either give load a contract, or add an explicit WC-4 exception for load that states its reason and removes it from the AC-1.2 Task list.
- **Priority.** High. P1 cannot close while this stands.

#### M1.b, from round1-b.md B2: B2. AC-1.1 and AC-1.2 cannot pass for /sc:load
- Expert: Wiegers (traceability across row, decision and check). Severity: MAJOR, graded blocking because two stated texts contradict each other.
- Location: spec:112 (load row, "Report: none (see note)"), spec:265 (decision: "a report file would be an unrequested addition"), spec:159 (P1 includes load), spec:183 (step 4), spec:195 (AC-1.1), spec:196 (AC-1.2).
- Issue: AC-1.1 requires every 3.1-3.2 command's Unattended section to name `return-contract.yaml` (spec:195). AC-1.2 runs step 4 for every P1 command (spec:196), and P1 includes load (spec:159). The load row and decision say load writes no report.
- Grading sentence: An implementer who follows the load row and the decision builds /sc:load with no contract, then AC-1.1 fails because its section cannot name a file it does not write, and AC-1.2 fails at step 4 because no contract exists; X is wrong because the spec contradicts itself on whether load reports a file.
- Recommendation: Either exempt load from AC-1.1 and AC-1.2 by name, or give load a contract. Choose one in section 3.2 and make AC-1.1 match.
- Priority: High. Quality impact: P1 cannot close with the spec as written.

### M2

#### M2.a, from round1-a.md B2: B2. AC-0.4 step 3 cannot pass in P0 (Adzic, testability)
- **Issue.** AC-0.4 says steps 1-3 and 5-7 pass in P0, with step 4 using the command's existing report (`spec:194`). Step 3 still requires that the `worker_done` report path is the WC-4 contract path and that the outcome matches the contract's status (`spec:182`). For `/sc:troubleshoot`, the report is `REPORT.md` (`spec:91`; `INV-B:242`). The contract arrives only in P1 (`spec:79`), and P0 forbids command edits (`spec:158`).
- **Grading sentence.** An implementer who runs AC-0.4 on `/sc:troubleshoot` in P0 finds that `worker_done`'s report path is `REPORT.md`, not a WC-4 contract path, so step 3 fails. P0 cannot pass without editing the command, which P0 forbids.
- **Evidence.** `spec:182`, `spec:194`, `spec:158`, `INV-B:49` and `INV-B:242`.
- **Expert.** Adzic (testable acceptance criteria).
- **Recommendation.** In P0, step 3 checks the outcome against the command's existing report. The contract-path check applies from P1. Alternatively, drop troubleshoot from AC-0.4.
- **Priority.** High. This is the P0 gate that tests the whole decision.

### M4

#### M4.a, from round1-b.md B1: B1. AC-0.4 cannot pass in P0 as written (steps 3 and 4)
- Expert: Adzic (examples and acceptance), Wiegers (testability). Severity: MAJOR, graded blocking because an acceptance criterion cannot pass.
- Location: spec:182 (step 3), spec:183 (step 4), spec:194 (AC-0.4), spec:159 (P1 scope).
- Issue: (a) Step 3 requires the report path to be "the WC-4 contract path" (spec:182). WC-4 arrives only in P1 (spec:159), so no P0 command can satisfy it. (b) AC-0.4 says step 4 "uses the command's existing report file" (spec:194), but step 4 parses the file as YAML and asserts `status` and `command` (spec:183). The workflow contract carries `status`, `plan_path`, `reflect_report_path` and no `command` key (INV-B:52, INV-B:272). Troubleshoot writes REPORT.md, and a return contract only with `--caller task-unified` (INV-B:49, INV-B:242). Adversarial has no fixed contract name (INV-A:35, INV-A:60). Step 4 therefore fails for troubleshoot and workflow, and step 3 fails for every P0 command.
- Grading sentence: An implementer who follows AC-0.4 as written runs `/sc:workflow` and `/sc:troubleshoot` in P0, then checks steps 3 and 4 on their existing report files, and both steps fail, so the P0 gate can never pass; X is wrong because the spec's own phase gate is unreachable and the text gives no pass path.
- Recommendation: In P0, check only what exists: the report file named by each command, plus steps 1, 2, 5, 6 and 7. Move the contract-field and WC-4 path checks (steps 3 and 4) to P1. Fix the adversarial contract name first (INV-A:60).
- Priority: High. Quality impact: the phase that tests the core decision (spec:43) cannot close.

### M5

#### M5.a, from round1-b.md B3: B3. Section 3.1 says the ready commands change only in the last column, but P1 and AC-1.1 require the flag on all of them
- Expert: Fowler (change scope), Wiegers (consistency). Severity: MAJOR, graded blocking because two stated texts contradict each other.
- Location: spec:79 ("The only command changes are the small fixes in the last column"), spec:84 (brainstorm, fix "None"), spec:87 (init-lite, fix "None"), spec:159 (P1: "the --unattended flag accepted by every command in sections 3.1 and 3.2"), spec:195 (AC-1.1).
- Issue: Brainstorm and init-lite have no change under spec:79, so an implementer following it adds no flag and no Unattended section to either. AC-1.1 requires the section in every 3.1 command, and P1 requires the flag.
- Grading sentence: An implementer who follows spec:79 leaves brainstorm and init-lite without `--unattended`, then AC-1.1 fails for both; X is wrong because P1 requires the flag on every 3.1 command, so the spec contradicts itself on the scope of change.
- Recommendation: Rewrite spec:79 to say that P1 adds `--unattended`, the Unattended section and the WC-4 contract to all ten 3.1 commands, and state the minimal change for brainstorm and init-lite.
- Priority: High. Quality impact: scope of change is misstated for 10 commands.

### M6

#### M6.a, from round1-b.md B4: B4. AC-2.2 cannot pass for five P2 commands whose gates resolve by default
- Expert: Adzic (examples), Nygard (failure resolution). Severity: MAJOR, graded blocking because an acceptance criterion cannot pass.
- Location: spec:200 (AC-2.2), spec:60 (WC-2 resolutions a, b, c), rows spec:100 (auggie-review), spec:103 (cleanup), spec:110 (improve), spec:116 (research), spec:118 (roadmap).
- Issue: AC-2.2 requires every P2 gate-trigger run to end `worker_done --outcome failed` with contract `status: blocked` and a non-empty `blocked_question` (spec:200). Under WC-2 resolution (a) the commands above do not block. Cleanup and improve apply non-approval items and list the rest (spec:103, spec:110). Auggie-review's `--unattended` implies `--no-post-pr` (spec:100). Research pins `--strategy planning` (spec:116). Roadmap resumes only when the flag is passed (spec:118). AC-2.2 also gives gate-trigger inputs only for tdd and cli-eval, with "for example" for the rest.
- Grading sentence: An implementer who follows AC-2.2 runs cleanup with input that hits its approval gate and expects a blocked contract and a failed outcome, but the row resolves the gate by listing the item and the run completes and reports succeeded; X is wrong because the criterion cannot pass for that command as written, and the same holds for the four others.
- Recommendation: Replace AC-2.2 with a per-command table: gate input, expected resolution (blocked, or (a)/(b) with success and a check that the listed items appear in the report), and expected `--outcome`.
- Priority: High. Quality impact: P2 acceptance is not testable for 5 of 15 commands.

### M7

#### M7.a, from round1-b.md B5: B5. AC-C1 cannot fail, and its scope conflicts with SA-2 and SA-5
- Expert: Fowler (boundary integrity), Wiegers (testability). Severity: MAJOR, graded blocking because the only check of a named safety boundary cannot detect the violation it names.
- Location: spec:172 (AC-C1), spec:147 (SA-2), spec:150 (SA-5), spec:180 (step 1, `ORCA` placeholder), spec:191-210 (phases that touch core).
- Issue: The pattern is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'`. In an -E pattern `\|` is a literal bar, not alternation. The check therefore matches only the text "orca orchestration|worktree|terminal|agent" and cannot match a real Orca call. I reproduced this by piping sample lines through the same expression (no files written): the line "orca orchestration worker-start" was not printed, and with an unescaped `|` the same line was printed. The check is also case-sensitive, so `ORCA orchestration` (the placeholder in spec:180) is missed. Second, AC-C1 scans `src/superclaude/core` (spec:172), where SA-5 requires the routing guide to gain an Orca section (spec:150) and where the contract file is allowed to mention Orca (spec:147). Once the pattern is fixed, both permitted texts would fail AC-C1 whenever they name an `orca` command.
- Grading sentence: An implementer who runs AC-C1 as written, in any phase, gets empty output whether or not a command contains `orca orchestration worker-start`, and then reports SA-2 and WC-8 as met; X is wrong because the only enforcement of the no-Orca-in-commands boundary can never fail.
- Recommendation: Use `grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b'`, scan `commands`, `skills` and `agents` for the hard rule, and scan `core` only for paths other than `WORKER-CONTRACT.md` and the routing-guide Orca section. State those two exclusions in SA-2 and SA-5. Add a self-test: the check must match a planted line.
- Priority: High. Quality impact: the boundary the spec relies on for standalone use (SA-2, spec:147) is unenforced.

## Noted, unactioned (verifier rejected; not prior blocking findings)

### M3 (verifier: The P1 Scope cell states "The WC-4 contract in unattended mode" with no command list, and line 79 says Phase 1 adds the contract to the ready commands. The four commands are therefore covered by that unqualified scope. The failure needs the P1 Commands column to be read as exhaustive for the contract, which is an extra assumption.)

#### M3.a, from round1-a.md B3: B3. The WC-4 contract has no phase for release-split, tdd, troubleshoot or init-lite (Fowler, architecture)
- **Issue.** The 3.1 intro says the ready commands report their named file "until Phase 1 adds the contract" (`spec:79`). P1 (`spec:159`) does not list release-split, tdd, troubleshoot or init-lite. Their rows give no contract: release-split reports `<output>/release-split-report.md` (`spec:89`; `INV-B:122`), tdd reports the TDD file (`spec:90`; `INV-B:222`), troubleshoot reports `REPORT.md` (`spec:91`), and init-lite writes `.dev/superclaude/context-audit.md` with "Small fix: None" (`spec:87`; `INV-A:55`). Their P2 fixes are prompt-gate changes only (`spec:89-91`), and P2's scope names gates only (`spec:160`). AC-2.3 runs 7.2 on each P2 command (`spec:201`), so step 4 (`spec:183`) fails for release-split, tdd and troubleshoot.
- **Grading sentence.** An implementer who follows `spec:79` expects Phase 1 to add the contract to every ready command, then finds that P1 does not list these commands and P2 does not mention a contract, so AC-2.3 step 4 fails for three commands. This needs no assumption beyond the spec's own text.
- **Expert.** Fowler (phase scope against interface).
- **Recommendation.** Assign each 3.1 command's contract to a named phase in its row, and make the `spec:79` intro match.
- **Priority.** High.

## Follow-up candidates

Listed in the two source reports above; not merged.

## Reviser brief

Blocking finding ids: M1, M2, M4, M5, M6, M7.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
