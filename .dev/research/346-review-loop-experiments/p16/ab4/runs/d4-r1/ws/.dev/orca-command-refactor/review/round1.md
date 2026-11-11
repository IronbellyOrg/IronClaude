review: 1 of 3

# Merged first review (coordinator; MERGE rule over two independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 f49af836e125e14e1ed8e3075d25d343db104880288ca930710a1a3cd03e7ad7
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 5ce82cc46d6f63b7785aac1ee5766218a35e594324ba969bd35545cc4d5023bb

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M1, M2, M3, M5, M6. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M4 (verifier: The quoted texts exist, but nothing says P1 may not add the flag/section to these three commands, so AC-1.1 can pass in P1 and "Phase 4 waits" and D3(a) concern only P4 changes; the claimed contradiction needs the extra assumption that a P1 flag amounts to deciding D2-D4.). The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M1

#### M1.a, from round1-a.md B1: B1 (blocking) CRITICAL-as-graded-by-consequence. Wiegers + Crispin. The P0 acceptance check cannot pass as written, and the next phase cannot start until it does.
- Quoted texts:
  1. `spec:182` (7.2 step 3): "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
  2. `spec:194` (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
  3. `spec:79`: "the worker reports the named file until Phase 1 adds the contract"; `spec:91` troubleshoot reports `REPORT.md`; `spec:92` workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml`; `spec:83` adversarial's contract "filename not fixed".
  4. Gate: `spec:154` "Later phases do not start until the earlier phase's checks in section 7 pass"; `spec:167` "A phase passes only when every check in its block and every common check passes."
- Stated wrong outcome: An implementer who follows the stated text as written runs the three P0 smoke commands, and each worker sends `worker_done --report-path` with the file the command writes today (`REPORT.md` for troubleshoot, the workflow ledger contract, an unnamed adversarial contract). Step 3 then fails for each, because no contract has `status` yet under WC-4's `<output-dir>/return-contract.yaml` (`spec:62`) and the reported path is not "the WC-4 contract path". AC-0.4 says step 3 must pass, and only step 4 is carved out. So AC-0.4 cannot be passed, P0 can never pass, and `spec:154` bars P1. The two texts contradict each other with no further assumption.
- Recommendation (narrow): in AC-0.4 carve out the "WC-4 contract" clauses of step 3 as well as step 4 (state that P0 compares `--outcome` with the command's own existing report), or move the "contract path" clause of step 3 into the P1+ checks. Delete rather than add.
- Priority: High. Quality impact: removes an unpassable gate on the smoke runs that the spec says test its core decision (`spec:158`, `spec:43`).

### M2

#### M2.a, from round1-b.md B1: B1 [CRITICAL-in-effect, expert: Crispin / Wiegers] AC-0.4 cannot pass: live-check step 3 demands a WC-4 contract that does not exist in Phase 0
- Stated text A: step 3 pass condition "exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (`spec:182`).
- Stated text B: AC-0.4 "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (`spec:194`); P0 makes no command edits (`spec:158`).
- An implementer who follows the stated text as written builds P0 smoke runs of `/sc:troubleshoot` (report `REPORT.md`, `spec:91`) and `/sc:adversarial` (contract filename "not fixed", `spec:83`) and then checks step 3. Step 3 requires the report path to be the WC-4 `return-contract.yaml` and the outcome to match its `status`; neither exists before P1, so step 3 cannot pass, and AC-0.4 exempts only step 4. The gate for P0 ("a failure here reopens section 1", `spec:194`) therefore fails for a reason unrelated to the decision it is meant to test.
- Recommendation: state in step 3 that, in P0, the report path is the command's existing report file and the outcome is judged from its own status; or exempt step 3's contract clauses in AC-0.4 as well.

### M3

#### M3.a, from round1-b.md B2: B2 [MAJOR, blocking, expert: Wiegers / Cockburn] AC-1.1 and AC-1.2 require a contract and an `## Unattended mode` section from `/sc:load`, which the spec says gets neither
- Stated text A: AC-1.1 "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (`spec:195`). `/sc:load` is a row of section 3.2 (`spec:112`).
- Stated text B: the `load` row gives Report "none (see note)", "use it as a step inside another worker's brief, not as its own Task" (`spec:112`); Decisions: "a report file would be an unrequested addition" (`spec:265`). P1 lists `load (usage line only)` (`spec:159`) but also says the P1 scope is "the WC-4 contract in unattended mode" for the section 3 commands (`spec:159`).
- An implementer who follows the text builds, for `load`, a usage-line fix only (rows 112, 159, 265). AC-1.1 then fails for `load` because no section naming `return-contract.yaml` exists, and AC-1.2 ("7.2 live check on each P1 command with `--unattended --output <dir>`", `spec:196`) fails at steps 3-4 (no `worker_done` contract path, `test -s <contract>` on a file that is never written). If the implementer instead adds the section and contract, the Decision at `spec:265` is violated.
- Recommendation: exclude `load` from AC-1.1/AC-1.2, or reverse the Decision.

### M5

#### M5.a, from round1-b.md B4: B4 [MAJOR, blocking, expert: Hohpe / Wiegers] WC-4's report location contradicts section 3 rows, so the section 7.2 steps 3-4 and AC-1.2 cannot pass for adversarial, workflow, cleanup-audit and index-repo
- Stated text A: WC-4 "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed", "known before dispatch" (`spec:62`); 7.2 step 3-4 check that path (`spec:182-183`); AC-1.2 runs every P1 command "with `--unattended --output <dir>`" (`spec:196`), and P1 includes fixes to adversarial, cleanup-audit, index-repo, workflow (`spec:159`).
- Stated text B (section 3.1):
  - adversarial: fix the contract to `<output>/adversarial/return-contract.yaml` (`spec:83`), a subdirectory, not `<output-dir>/return-contract.yaml`. AC-1.4 only asks that "adversarial names one fixed path" (`spec:198`), so it does not choose between the two.
  - workflow: brief passes only `--handoff none`; the contract is at `.dev/tasks/to-do/<id>/return-contract.yaml` (`spec:92`; INV-B workflow entry, `commands-b.md` line 52 of the table and the `/sc:workflow` (d) note: id is generated by the command, and the contract is "Not written for pre-creation STOPs"). The path is not known before dispatch, no output directory is passed, and for a pre-creation STOP no `<id>` directory exists, so the "write the contract for pre-creation STOPs too" fix (`spec:92`, AC-1.4) has no stated location.
  - cleanup-audit: "output dir is fixed" `.claude-audit/` (`spec:85`), so no `--output <dir>` exists to pass.
  - index-repo: brief passes "none", location only implied, and the P1 fix is "State the output location" (`spec:86`); no output flag is added although P1 says "output flags for commands that lack one" (`spec:159`).
- An implementer who follows the stated text builds, for these four, a contract at the place section 3 names. WC-4, step 3 ("report path is the WC-4 contract path"), step 4 (`test -s <contract>`) and AC-1.2 then point at a path that is not where the file is, or at an `--output` flag that the command does not accept. The criteria cannot pass as written for those four commands, and the adversarial rows contradict WC-4 directly.
- Recommendation: add to WC-4 the exception list (path per command, coordinator-known), or fix each command's contract to `<output-dir>/return-contract.yaml` and give workflow, cleanup-audit and index-repo an output flag.

### M6

#### M6.a, from round1-b.md B5: B5 [MAJOR, blocking, expert: Crispin / Adzic] AC-2.2 requires every P2 command to end `blocked` with a `blocked_question`; several P2 commands have no blocking path
- Stated text A: AC-2.2 "Gate-trigger run per P2 command ... `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`" (`spec:200`). P2 lists auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot (`spec:160`).
- Stated text B: the gate resolution of several of these is not "blocked":
  - research: `--unattended` "pins `--strategy planning`" (`spec:116`);
  - tasklist: Stage 10.5 "passes `--unattended` to each reflect so the headless rule applies" (`spec:122`);
  - auggie-review: implies `--no-post-pr` and `--no-remediation-offer` (`spec:100`);
  - cleanup and improve: apply only items outside "Approval Required", list the rest (`spec:103,110`);
  - reflect: follows "the existing headless auto-accept rule" (`spec:88`).
- An implementer who follows the text builds those commands to complete with a default; no input makes them write `status: blocked`. AC-2.2 therefore cannot pass for them as written, and AC-2.1 ("one assertion per gate listed in the section 3 row") and AC-2.3 are the only checks that can. The example inputs in AC-2.2 (`tdd "auth"`, `cli-eval run` without `--suite`) fit only the blocked-type commands.
- Recommendation: restrict AC-2.2 to the commands whose row says "blocked", and give the default-resolution commands a check of their own (the default applied, no `agentWait`).

## Noted, unactioned (verifier rejected; not prior blocking findings)

### M4 (verifier: The quoted texts exist, but nothing says P1 may not add the flag/section to these three commands, so AC-1.1 can pass in P1 and "Phase 4 waits" and D3(a) concern only P4 changes; the claimed contradiction needs the extra assumption that a P1 flag amounts to deciding D2-D4.)

#### M4.a, from round1-b.md B3: B3 [MAJOR, blocking, expert: Fowler / Cockburn] AC-1.1 and the P1 scope require an unattended section on `pr-submit`, `implement` and `post-release`, but the recommended decisions D2-D4 and Phase 4 say those commands are not changed or are not workers
- Stated text A: AC-1.1 covers "every command in sections 3.1-3.2" (`spec:195`); P1 scope "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (`spec:159`). `pr-submit`, `implement`, `post-release` are rows of section 3.2 (`spec:109,113,114`).
- Stated text B: Phase 4 owns them and "waits for answers to D2-D4" (`spec:154,162`); D3 recommendation (a) "Coordinator or person only ... no pr-submit changes in Phase 4" (`spec:240-242`); section 4 says `pr-submit` "stays a worker candidate only if the user accepts open decision D3" (`spec:139`); the same section gives coordinator-only commands "no `--unattended` mode" (`spec:128`).
- An implementer who follows the text builds, for the recommended D3(a), no pr-submit change in P4, but AC-1.1 in P1 requires a `## Unattended mode` section in `pr-submit.md`. Both cannot hold: either P1 gives pr-submit a worker mode before the user has decided (contradicting "Phase 4 waits"), or AC-1.1 fails. The same holds for `implement` (D2) and `post-release` (D4) whenever P1 requires the flag but the gate resolution (`spec:109,113`) arrives only in P4.
- Recommendation: restrict P1/AC-1.1 to the commands whose phase is P1-P3, or move the flag acceptance for the P4 commands into P4.

## Follow-up candidates

Listed in the two source reports above; not merged.

## Reviser brief

Blocking finding ids: M1, M2, M3, M5, M6.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
