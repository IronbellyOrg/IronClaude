review: 1 of 3

# Merged first review (coordinator; MERGE rule over three independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 eaf960aa84240881dd95b7d715d88f0a1ec4cf2a455decf0840cbaafe3e395c0
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 79a8b342bd1be83a0db0588b3b347216e0b53ee4432b6ca1711cb5732028f137
- .dev/orca-command-refactor/review/round1-c.md verdict FAIL sha256 4cf024041a352973924fc0a86d9922264fdcd0f14ab0bd47dab5205d01374a68

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M1, M2, M3, M6, M7, M8, M9, M11, M12, M13. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M4 (verifier: The texts conflict (row 88 against SA-6 and item 9). The stall branch depends on UNVERIFIED item 9 and is a WC-2 issue, not the stated safety outcome. The safety branch needs two things the candidate does not supply: a re-keying of the trigger, which SA-6 says is not done, and a statement that `--remediate` applies code, which row 88 never gives. D2 governs the implement Ruling, not reflect remediation.); M5 (verifier: As written, AC-C1's pattern does not match `orca orchestration check` at all (tested: exit 1), so the premise that AC-C1 flags P0 text does not hold for the spec's own regex. Under the intended plain-bar regex, a match needs P0 text in the form `orca` followed by orchestration, worktree, terminal or agent. SA-2 permits an Orca "mention" but no candidate text requires that form, so the failure is conditional on wording the spec leaves open.); M10 (verifier: The texts conflict in intent, but AC-1.1 only checks that the section names `return-contract.yaml`. A load section that names it and states that no contract is written satisfies the check as written. The candidate does not say AC-1.1 fails for load, so "the criterion cannot pass" does not follow.). The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M1

#### M1.a, from round1-a.md ARCH-1: ARCH-1 (blocking): WC-4's `<output-dir>/return-contract.yaml` rule cannot be applied to the rows that define their own output
- Severity: MAJOR. Expert: Fowler (interface), Hohpe (message contract between worker and coordinator).
- Location: `specs/orca-worker-contract-spec.md:62` (WC-4: contract at `<output-dir>/return-contract.yaml`, "known before dispatch"). `:73` (section 2.3: the brief names the output directory "so the report path is known before dispatch"). `:83` (adversarial: "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"). `:87` (init-lite: `--output <file>`). `:90` (tdd: `--output <file>`; "the TDD at `--output`"). `:92` (workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`; no output flag). `:116` (research: "contract naming the generated `claudedocs/research_*.md` path"). `inventory/commands-b.md:47` (tdd `--output` is a file). `inventory/commands-b.md:52` (workflow contract location).
- Issue: WC-4 defines the contract as a file in a directory named by `--output`. Four rows contradict that: adversarial puts it in a subdirectory, init-lite and tdd treat `--output` as a file, workflow has no output directory, and research generates its path at run time. The coordinator follows section 2.3 and opens a path that does not exist, or writes into a file path.
- Grading check: "An implementer who follows WC-4 and section 2.3 for tdd passes `--output <file>` as a directory, so the contract path is `<file>/return-contract.yaml`, which cannot be written; for adversarial the coordinator opens `<output-dir>/return-contract.yaml`, which does not exist." Blocking: two stated texts contradict, and the coordinator reads the wrong file.
- Recommendation: define the contract path per command in section 3 (one column), keep `<output-dir>/return-contract.yaml` only for commands whose `--output` is a directory, and say how the coordinator learns the path for workflow and research before dispatch (for example, the brief passes `--contract <path>`).
- Priority: High. Quality impact: consistency 4 to 7.

### M2

#### M2.a, from round1-a.md ARCH-2: ARCH-2 (blocking): the P1 change to workflow writes a contract in standalone mode, which SA-3 forbids
- Severity: MAJOR. Expert: Fowler, Nygard (partial-run safety).
- Location: `specs/orca-worker-contract-spec.md:148` (SA-3: "The new contract file and report files are written only in unattended mode or when the caller passes the new output flag"). `:92` (workflow row: "Write the contract for pre-creation STOPs too (WC-4 'every outcome') (P1)"). `:62` (WC-4 applies "In unattended mode"). `inventory/commands-b.md:52` and `:272` (workflow writes no contract for pre-creation STOPs today; the contract is written only after the package exists).
- Issue: SA-3 says standalone runs write no new contract files. The P1 workflow change writes one on a pre-creation STOP, which is standalone behaviour. Because the STOP happens before the package exists, the spec also gives no location for the file.
- Grading check: "An implementer who builds the P1 workflow change writes `return-contract.yaml` in a person's tree on a plain `/sc:workflow` STOP, and cannot choose a directory for it; SA-3 says that must not happen." Blocking: it violates a hard requirement stated as holding in every phase (`:141`).
- Recommendation: gate the pre-creation contract on `--unattended` (and a `--output` directory), name its location, or drop it from P1.
- Priority: High. Quality impact: consistency +3.

### M3

#### M3.a, from round1-a.md ARCH-3: ARCH-3 (blocking): P1 accepts `--unattended` on commands whose outward defaults stay on until P2 or P4
- Severity: MAJOR. Expert: Nygard (safety boundary), Newman (interface evolution).
- Location: `specs/orca-worker-contract-spec.md:159` (P1: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"). `:100` (auggie-review: posts to the PR by default; the change is phase P2). `:121` (task: commit and push by default; phase P2). `:113-114` (post-release and pr-submit: phase P4). `:67` (WC-9: under `--unattended`, outward defaults "are off"). `inventory/commands-a.md:38` (auggie-review posts by default with no prompt). `inventory/commands-b.md:94`, `:297` (pr-submit and task outward actions).
- Issue: the "no-op" caveat applies only to commands with no gate. auggie-review has gates and an outward default, so in P1 `/sc:auggie-review <PR> --unattended` is accepted and still posts to GitHub. WC-9 says it must not.
- Grading check: "An implementer who ships P1 and runs `/sc:auggie-review <PR> --unattended` as the brief allows gets a posted review on the PR, which WC-9 forbids; the phase text says the flag is accepted with no change in behaviour." Blocking: outward action from a flag the spec says is safe.
- Recommendation: in P1, reject `--unattended` with an error for every command that has an outward default until its P2 or P4 change lands, or move the outward-default change for auggie-review and task into P1.
- Priority: High. Quality impact: consistency +3.

### M6

#### M6.a, from round1-a.md REQ-2: REQ-2 (blocking): AC-0.4 step 4 cannot pass for `/sc:troubleshoot`
- Severity: MAJOR. Expert: Adzic (acceptance examples), Wiegers.
- Location: `specs/orca-worker-contract-spec.md:194` (AC-0.4: "step 4 uses the command's existing report file"), `:183` (step 4: `test -s <contract>` and a YAML parse asserting `d['status']` and `d['command']`), `:91` (troubleshoot row: today's report is `REPORT.md` (`report_path`)). `inventory/commands-b.md:49` and `:242` (troubleshoot writes `REPORT.md`; `return-contract.yaml` only with `--caller task-unified`).
- Issue: step 4 requires a YAML file with `status` and `command`. For troubleshoot the existing report is a Markdown `REPORT.md` with no such keys, and the contract exists only under `--caller task-unified`, which the P0 brief does not pass. The check fails on a correct run.
- Grading check: "An implementer who runs AC-0.4 as written on troubleshoot builds a correct run, runs step 4, and the YAML parse fails; this is wrong because the criterion checks a file type the command does not write." Blocking: an acceptance criterion cannot pass.
- Recommendation: define step 4 per command for P0 (troubleshoot checks that `REPORT.md` exists and is non-empty, with `status` from the worker's `worker_done` instead), or replace troubleshoot in the P0 set with a command that writes the YAML contract today (adversarial or workflow).
- Priority: High. Quality impact: testability 5 to 7.

#### M6.b, from round1-b.md B5: B5. CRITICAL. AC-0.4 step 4 cannot pass for `/sc:troubleshoot` as written
- **Issue.** AC-0.4 (`spec:194`) says step 4 "uses the command's existing report file", because the contract arrives in P1. Step 4 (`spec:183`) asserts that the file is YAML with `status` in the four-value set and a `command` key. Troubleshoot's report is `REPORT.md` (`commands-b.md:49`, `:242`). Its `return-contract.yaml` appears only with `--caller task-unified` (`commands-b.md:242`). Workflow's `return-contract.yaml` does have a `status` (`commands-b.md:272`), but its values are not listed in the inventory (UNVERIFIED).
- **Grading sentence.** An implementer who runs step 4 on the troubleshoot `REPORT.md` gets a YAML or missing-key error, so AC-0.4 cannot pass for that command.
- **Expert.** Adzic (example check that does not match its own data). Wiegers (acceptance criteria).
- **Recommendation.** Limit step 4 in P0 to commands whose existing report is YAML with the four-value status, or check file presence only for the rest. Name which commands use which form.
- **Priority.** High. **Quality impact.** Medium-high: the P0 phase gate cannot close.

### M7

#### M7.a, from round1-b.md B1: B1. CRITICAL. WC-3 lets a coordinator answer add a flag; WC-9 says only the brief can turn on an outward action
- **Issue.** WC-3 says that after an ask the command is re-invoked "with the answer as a flag" (`spec:61`). WC-9 says an outward action "turns on only through the command's own explicit flag written in the brief" (`spec:67`). D4 says the coordinator may authorize outward actions only with the user's own instruction quoted in the brief (`spec:245-247`). The first two texts allow a flag that is not in the brief. The third forbids it.
- **Grading sentence.** An implementer who follows WC-3 on the post-release gate (`spec:113`, blocked on outward confirmations) re-invokes the command with an ask reply supplied as the push flag, and the outward push runs although no such flag is in the brief, which WC-9 (`spec:67`) forbids.
- **Expert.** Wiegers (contradictory requirements). Whittaker, FR-2.3 Sentinel Collision: a reply carries a value that an outward gate reads as authorization.
- **Recommendation.** Limit WC-3 answers to gate values that are not outward. Any outward flag comes only from the brief, as D4 says. Put that rule in WC-3 and WC-9 with the same wording.
- **Priority.** High. **Quality impact.** High: a safety-boundary risk.

### M8

#### M8.a, from round1-b.md B2: B2. CRITICAL. The AC-C1 grep cannot fail, so SA-2 and WC-8 have no working gate
- **Issue.** AC-C1 (`spec:172`) uses `\|` inside `grep -E`. In an extended regex `\|` is a literal bar, not alternation. I ran the pattern as written against a violating line, `orca orchestration check --json`, and it printed nothing (exit 1). The same pattern with plain `|` matched (exit 0). AC-C1 therefore passes on any command that calls Orca.
- **Grading sentence.** An implementer who adds `orca orchestration check` to a command and runs AC-C1 as written gets empty output and records SA-2 (`spec:147`) and WC-8 (`spec:66`) as passed.
- **Expert.** Wiegers (acceptance check). Crispin (completeness of the check).
- **Recommendation.** Use plain `|` inside the group. Add a positive control: the check must match a planted line in a scratch file. Re-run it before P0 is accepted.
- **Priority.** High. **Quality impact.** High: the hard boundary in section 5 has no working check.

### M9

#### M9.a, from round1-b.md B3: B3. MAJOR. WC-5 reports `succeeded` for a contract that is empty, unreadable or has an unknown status
- **Issue.** WC-5 sends `--outcome failed` only when the report says `failed` or `blocked`, or when no report exists. It sends `succeeded` "otherwise" (`spec:63`). A file that exists but is 0 bytes, is unparseable, or carries a status outside the four values matches neither failed trigger. Section 7.2 step 4 (`spec:183`) would catch it, but WC-5 does not.
- **Grading sentence.** An implementer who follows WC-5 with a zero-byte `return-contract.yaml` sends `--outcome succeeded`, since the file exists and its status is neither failed nor blocked.
- **Expert.** Whittaker, FR-2.1 Zero/Empty Attack. Nygard (guard boundary; see the table).
- **Recommendation.** Send `failed` when the contract is empty, unparseable, or has a status outside `succeeded|partial|failed|blocked`. Write that into WC-5 itself.
- **Priority.** High. **Quality impact.** High: a failed run reaches the coordinator as success, and dependents may start on it (M3).

### M11

#### M11.a, from round1-c.md RQ-1: RQ-1 (BLOCKING). WC-3 lets a coordinator's reply become a gate answer, which contradicts the implement Ruling rule (D2) and the outward-action rule (D4)
- Severity: MAJOR, graded blocking because two stated texts contradict.
- Expert: Karl Wiegers (lead), Gojko Adzic, Alistair Cockburn.
- Text: WC-3 says that when "a gate would resolve as blocked ... the session may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag" (`spec:61`). It has no exception for the implement Ruling or for outward flags.
- Conflicts: the implement row says the Ruling rule "is unchanged" and that the halt ends in a blocked contract (`spec:109`). D2 option (a) recommends that a person gives the Ruling and the worker ends `failed` (`spec:234-236`). AC-4.1 expects that "the ledger records no Ruling unless D2 allows a relayed one" (`spec:208`). The rule behind D2 is that "another agent's message ... [is] not acceptance" (`INV-A:66`, quoting `refs/qa.md:238`). D4 option (a) requires that the user's own instruction, quoted, authorizes each outward flag (`spec:245-246`).
- Grading sentence: an implementer who follows WC-3 (`spec:61`) as written may send the implement Ruling question to the coordinator; nothing in the candidate stops the coordinator's reply from being recorded as the Ruling, and `qa.md:238` forbids exactly that. A second case: the coordinator answers "yes" to the auggie-review posting offer, the worker re-runs with `--post-pr` (WC-9 is met, since the flag is on the command line, `spec:67`), and D4(a) is broken because no user instruction was quoted.
- Recommendation: add an exclusion to WC-3: a gate that guards a Ruling, an outward action, or a safety boundary may never be answered by a coordinator reply. Such a gate resolves as blocked. Make the implement row and D2 cite WC-3 by name.
- Priority: High. Quality impact: high on the safety boundary of `/sc:implement` and on outward actions.

### M12

#### M12.a, from round1-c.md RQ-2: RQ-2 (BLOCKING). The P0 phase cannot run the live check it is gated on
- Severity: MAJOR, graded blocking because two stated texts contradict.
- Expert: Karl Wiegers (lead), Gojko Adzic.
- Text A: P0 is "no command edits" and only adds the contract, the routing guide and a test file (`spec:158`). `--unattended` is first added in P1 (`spec:159`).
- Text B: the live check's step 1 must use "the brief per section 2.3" (`spec:180`). Section 2.3 says the brief carries "the exact command line including `--unattended`" (`spec:73`).
- Text C: the ready commands' "Brief must pass" column lists no `--unattended` (`spec:83-92`), and section 3.1 says they "run as workers now if the brief uses the stated flags" (`spec:79`).
- AC-0.4 then requires steps 1-3 and 5-7 to pass for `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` (`spec:194`).
- Grading sentence: an implementer who follows `spec:180` for P0 puts `--unattended` on the `/sc:troubleshoot` line. P0 adds no such flag (`spec:158`), so the run is not unattended, and AC-0.4 passes a decision test that never exercised the WC-2 and WC-4 behaviour that the decision depends on.
- Recommendation: state the P0 brief for ready commands without `--unattended` and say that the P0 run tests only the default path. Or move the P0 live check to after the first P1 command. Make `spec:73` and `spec:79` say the same thing.
- Priority: High. Quality impact: high on phase gating (the decision in section 1 is tested by this run).

### M13

#### M13.a, from round1-c.md AR-1: AR-1 (BLOCKING). Two ready verdicts keep fixed output paths, which breaks WC-11 in the default shared worktree
- Severity: MAJOR, graded blocking because two stated texts contradict.
- Expert: Martin Fowler (lead), Sam Newman.
- Text: WC-11 says "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes" (`spec:69`). The brief places workers in the current worktree by default (`CAPS:115`). Section 3.1 nonetheless marks cleanup-audit "ready" with a fixed output directory (`spec:85`, `INV-A:42`, and the verdict basis at `INV-A:107`: fixed `.claude-audit/pass1-summary.md`), and index-repo "ready" with `PROJECT_INDEX.md` at a location that is itself UNVERIFIED (`spec:86`, `INV-A:53`). Cleanup-audit's `progress.json` is also fixed (`INV-A:42`). The row's note "one audit per worktree at a time (WC-11)" (`spec:85`) is not a rule in section 2.3 (`spec:73`) or in the brief template.
- Grading sentence: an implementer who follows `spec:85` and `spec:86` dispatches two cleanup-audit or index-repo workers into the default shared worktree, and both write the same `.claude-audit/pass1-summary.md` or `PROJECT_INDEX.md`, which WC-11 says must never happen. Neither the brief template nor any check stops the second dispatch.
- Recommendation: move both rows to "needs change" until the output path takes a per-run slug, or add a coordinator rule (one such Task per worktree at a time) to section 2.3 and to AC-C1 or a new check.
- Priority: High. Quality impact: high (silent clobbering of shared state).

## Noted, unactioned (verifier rejected; not prior blocking findings)

### M4 (verifier: The texts conflict (row 88 against SA-6 and item 9). The stall branch depends on UNVERIFIED item 9 and is a WC-2 issue, not the stated safety outcome. The safety branch needs two things the candidate does not supply: a re-keying of the trigger, which SA-6 says is not done, and a statement that `--remediate` applies code, which row 88 never gives. D2 governs the implement Ruling, not reflect remediation.)

#### M4.a, from round1-a.md ARCH-4: ARCH-4 (blocking): the P2 reflect change makes a worker self-approve code remediation, which D2 forbids for implement
- Severity: MAJOR. Expert: Nygard, Fowler (who decides).
- Location: `specs/orca-worker-contract-spec.md:88` (reflect, P2: "Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt"). `:122` (tasklist: "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies"). `:151` (SA-6: the headless rule keys on `claude --print` and "`--unattended` reuses it and does not replace it"). `:232-236` (D2: an agent must not approve its own work; "the rule exists to stop an agent approving its own work"). `:280` (UNVERIFIED 9: an Orca worker is "assumed" not headless). `inventory/commands-b.md:109`, `:310` (the headless rule keys on `claude --print` with no TTY).
- Issue: the spec applies the headless auto-accept to a worker, which is not headless by the spec's own assumption (`:280`). Either the trigger is re-keyed to `--unattended` (which the spec says it does not do, `:151`) or the prompt stalls (contrary to WC-2). If it fires, a worker auto-accepts remediation that may edit code, which D2 forbids for implement. The spec does not say whether Stage 10.5 still passes `--remediate`.
- Grading check: "An implementer who follows row 88 either stalls the reflect worker at the prompt or re-keys the headless rule, and in the second case a worker applies code remediation without a person, which D2 says must not happen." Blocking: safety-boundary risk stated in the spec's own rationale.
- Recommendation: state the trigger for `--unattended` explicitly, state that remediation is never auto-accepted under `--unattended` (the gate resolves as blocked, per WC-2 (c)), and state whether Stage 10.5 drops `--remediate`.
- Priority: High. Quality impact: consistency +3.

### M5 (verifier: As written, AC-C1's pattern does not match `orca orchestration check` at all (tested: exit 1), so the premise that AC-C1 flags P0 text does not hold for the spec's own regex. Under the intended plain-bar regex, a match needs P0 text in the form `orca` followed by orchestration, worktree, terminal or agent. SA-2 permits an Orca "mention" but no candidate text requires that form, so the failure is conditional on wording the spec leaves open.)

#### M5.a, from round1-a.md REQ-1: REQ-1 (blocking): the common acceptance check AC-C1 cannot pass in the phase that adds the contract
- Severity: MAJOR. Expert: Wiegers (testability), Adzic (acceptance examples).
- Location: `specs/orca-worker-contract-spec.md:172` (AC-C1 greps `src/superclaude/core` for Orca verbs and excludes only `ccsession-tag`). `:158` (P0 adds `src/superclaude/core/WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`). `:147` (SA-2 allows an Orca mention "inside the contract file" as an example of the question channel). `:150` (SA-5, routing-guide Orca section).
- Issue: AC-C1 is a common check that every phase must pass (`:169-176`, "A phase passes only when every check in its block and every common check passes"). Its grep covers `src/superclaude/core`. P0 puts the contract file and an Orca section in that directory, and SA-2 expects the contract file to name the Orca question channel. Both produce `orca orchestration ...` text that AC-C1 matches. AC-C1 therefore fails at P0 by design.
- Grading check: "An implementer who follows the stated text as written builds the P0 contract file and the routing-guide Orca section, runs AC-C1, and gets a match, so P0 cannot pass; this is wrong because the common check is a stated pass condition for every phase." Blocking: an acceptance criterion cannot pass.
- Recommendation: exclude `WORKER-CONTRACT.md` (and the Orca section, or name its file) from AC-C1, or change AC-C1 to forbid Orca verbs in command and skill files only, matching SA-2's wording. State the exclusion in one place.
- Priority: High. Quality impact: testability 6 to 8 once fixed.

### M10 (verifier: The texts conflict in intent, but AC-1.1 only checks that the section names `return-contract.yaml`. A load section that names it and states that no contract is written satisfies the check as written. The candidate does not say AC-1.1 fails for load, so "the criterion cannot pass" does not follow.)

#### M10.a, from round1-b.md B4: B4. CRITICAL. AC-1.1 cannot pass for `/sc:load`
- **Issue.** AC-1.1 (`spec:195`) requires every command in sections 3.1 and 3.2 to have a `## Unattended mode` section that names `return-contract.yaml`. The `load` row (`spec:112`) says the report is "none (see note)" and the Decisions table (`spec:265`) says a report file for load "would be an unrequested addition". Both texts are explicit.
- **Grading sentence.** An implementer who follows the load row writes no contract, so AC-1.1 fails on `load`, and the criterion cannot pass as written.
- **Expert.** Wiegers (traceability between decision and check).
- **Recommendation.** Exempt `load` from AC-1.1 by name, and say in P1 (`spec:159`) that load gets the flag as a usage-line fix only.
- **Priority.** High. **Quality impact.** Medium-high: an implementer stops at a failing gate or edits the check.

## Follow-up candidates

Listed in the three source reports above; not merged.

## Reviser brief

Blocking finding ids: M1, M2, M3, M6, M7, M8, M9, M11, M12, M13.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
