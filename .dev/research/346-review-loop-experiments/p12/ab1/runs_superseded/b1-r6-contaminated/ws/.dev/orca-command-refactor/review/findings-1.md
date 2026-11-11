Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md F1)
### F1 - CRITICAL (blocking) - Wiegers - load: acceptance check and phase scope contradict the load row
- Texts: AC-1.1 requires "every command in sections 3.1-3.2" to have a `## Unattended mode` section "naming `return-contract.yaml`" (`SPEC:195`); section 3 says every changed command gains that section (`SPEC:76`); P1 lists "load (usage line only)" (`SPEC:159`) and the load row says report "none (see note)", "use it as a step inside another worker's brief, not as its own Task", change is the usage line only (`SPEC:112`); the Decisions row says "a report file would be an unrequested addition. Only its usage-line defect is fixed" (`SPEC:265`). WC-4 says the contract is written on every outcome (`SPEC:62`).
- Grading sentence: An implementer who follows the stated text as written builds, for /sc:load, either a usage-line fix only (`SPEC:112,159,265`), which fails AC-1.1 (`SPEC:195`), or an `## Unattended mode` section naming `return-contract.yaml` (`SPEC:195`, `SPEC:62`), which adds the report file that `SPEC:265` rules out; one of the two stated texts must lose, and the phase check cannot pass while both stand.

### M2

#### M2.a (round1-a.md F2)
### F2 - CRITICAL (blocking) - Crispin/Wiegers - AC-0.4 requires a step-3 condition that Phase 0 cannot meet
- Texts: AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (`SPEC:194`); step 3 passes only if "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (`SPEC:182`); P0 contains "no command edits" (`SPEC:158`) and the WC-4 contract is a P1 deliverable (`SPEC:159`). The three P0 commands: troubleshoot reports `REPORT.md` with no `status` (B:242, `SPEC:91`), workflow's contract sits at `.dev/tasks/to-do/<id>/` (`SPEC:92`), adversarial's filename is not fixed until P1 (`SPEC:83`).
- Grading sentence: An implementer who follows the stated text as written runs the P0 smoke runs and applies step 3 to them, and the run cannot pass, because no P0 command writes a WC-4 contract at the WC-4 path; the phase gate "later phases do not start until the earlier phase's checks pass" (`SPEC:154`) then blocks the whole rollout, and the sentence at `SPEC:194` ("a failure here reopens section 1") would reopen the decision on a defect of the check.

#### M2.b (round1-b.md B1)
### B1 (CRITICAL; Wiegers, Adzic, Whittaker) Phase 0 acceptance check AC-0.4 cannot pass as written
Stated texts that contradict:

- Spec line 182 (7.2 step 3): "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Spec line 194 (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
- Spec line 158 (P0): the three smoke commands are `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --output <dir>`, run before any command edit.
- Spec line 91 (3.1 troubleshoot): its report today is `REPORT.md`, with no contract. Spec line 83: adversarial's contract filename "not fixed". The WC-4 contract is added only in P1 (spec line 159).

Wrong outcome: an implementer who follows the stated text builds a P0 gate that requires step 3 to pass, so the worker's report path must be the WC-4 contract path and the outcome must match the contract's `status`. For `/sc:troubleshoot` no such contract exists in P0, and the spec says it arrives in P1. AC-0.4 carves out only step 4, not step 3. The P0 smoke runs can therefore never pass. Line 154 says later phases do not start until the earlier phase's checks pass, and line 194 says "a failure here reopens section 1", so a correct run triggers the reopen rule. Fix by relaxing step 3 for P0 to "the report path is the command's existing report file", the same carve-out given for step 4.

### M3

#### M3.a (round1-a.md F3)
### F3 - CRITICAL (blocking) - Adzic - cli-portify: the happy-path check cannot pass, because every gate resolves only as blocked
- Texts: cli-portify row: "each of the three approval gates resolves as blocked", resume via `--resume <contract>` (`SPEC:105`); the gates are always on (A:45); WC-2 allows three resolutions (default, caller flag, blocked) (`SPEC:60`), but the row picks only the third and lists no flag that carries an approval; AC-2.3: "Happy-path run per P2 command with every required flag in the brief ... 7.2 passes with `--outcome succeeded`" (`SPEC:201`) and P2 contains cli-portify (`SPEC:160`).
- Grading sentence: An implementer who follows the stated text as written builds a cli-portify that stops as blocked at the first approval gate on every unattended run and, on resume, reaches the same gate again, because no listed flag or contract field records an approval; AC-2.3 requires a `succeeded` run, which that build can never produce.

### M4

#### M4.a (round1-b.md B2)
### B2 (MAJOR; Wiegers, Fowler) `/sc:load`: the per-command table and the P1 acceptance check contradict each other
Stated texts that contradict:

- Spec line 112 (3.2 load row): Report (WC-4) "none (see note)"; "use it as a step inside another worker's brief, not as its own Task"; Phase "P1 (usage line only)".
- Spec line 159 (P1): "`load` (usage line only)".
- Spec line 265 (Decisions): "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- Spec line 195 (AC-1.1): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `load` is in section 3.2, line 112.
- Spec line 76: "Every changed command also gains the `## Unattended mode` section". Line 159 also says `--unattended` is accepted "by every command in sections 3.1 and 3.2", including `load`.

Wrong outcome: an implementer who does exactly what the load row and the Decisions row say (fix the Usage line only, add no report) fails AC-1.1, because the test requires an Unattended-mode section naming `return-contract.yaml` in `cmd/load.md`. An implementer who satisfies AC-1.1 adds a contract and a section to `load`, which line 265 calls an unrequested addition and line 112 says is not needed. AC-1.1 has no exception for `load`, so P1 cannot pass without breaking one of the two stated texts. Fix by naming `load` as the exception in AC-1.1, or by removing `load` from the "every command in 3.1-3.2" scope.

#### M4.b (round1-c.md F1)
### F1. BLOCKING (CRITICAL). `/sc:load` is required to carry a contract section by AC-1.1 and is also given no report
Stated texts:
1. SPEC:195: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". SPEC:76: "Every changed command also gains the `## Unattended mode` section". SPEC:159: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
2. SPEC:112: the `load` row is in section 3.2 with Report "none (see note)", Resume "n/a", Other change "use it as a step inside another worker's brief, not as its own Task".
3. SPEC:265 (Decisions): "a report file would be an unrequested addition".
Grading check: An implementer who follows the stated text as written builds a `load` that either (a) carries an `## Unattended mode` section naming `return-contract.yaml` (so AC-1.1 passes), which means `load` writes or promises a contract that SPEC:112 and SPEC:265 say it must not have, or (b) carries no such section as SPEC:112 and SPEC:265 say, and then AC-1.1 and AC-1.2 (SPEC:196: "7.2 live check on each P1 command", whose step 4 SPEC:183 requires a contract file) cannot pass. The acceptance criterion cannot pass with the row as written, and the two stated texts contradict.

### M5

#### M5.a (round1-c.md F2)
### F2. BLOCKING (CRITICAL). AC-1.1 at Phase 1 requires contract sections whose content waits on decisions D2-D4, which the spec says Phase 1 does not need
Stated texts:
1. SPEC:154: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4." SPEC:162: Phase 4 = implement, post-release, pr-submit, "needs the user's decision first".
2. SPEC:195 (P1, AC-1.1): every command in sections 3.1-3.2 has the section; SPEC:159: P1 = "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". `implement` (SPEC:109), `post-release` (SPEC:113) and `pr-submit` (SPEC:114) are in section 3.2.
3. SPEC:52: each section "lists only its own gate resolutions and report file". Those resolutions for the three commands are "open decision D2", "(open decision D4)" and "per open decision D3" (SPEC:109, 113, 114).
4. SPEC:241 (D3, recommended (a)): "no pr-submit changes in Phase 4". SPEC:139: `/sc:pr-submit` "stays a worker candidate only if the user accepts open decision D3".
Grading check: An implementer who follows the stated text as written builds, in Phase 1, `## Unattended mode` sections for `implement`, `post-release` and `pr-submit`, to make AC-1.1 pass. Those sections must list gate resolutions that SPEC:109-114 and SPEC:154 make depend on answers not yet given, so the implementer either invents the answers (contradicting SPEC:154 and the D2-D4 text) or writes sections that advertise a worker mode the recommended D3(a) says does not exist. The same applies to the Phase 2 and Phase 3 commands: Phase 1 would accept `--unattended` on `/sc:task` (SPEC:121) while its gates (confidence below 0.70, TFEP) still prompt until Phase 2, which breaks the WC-2 promise (SPEC:60) and the claim that each phase "is independently useful" (SPEC:155). The acceptance criterion and the phase plan contradict.

### M6

#### M6.a (round1-c.md F3)
### F3. BLOCKING (CRITICAL). WC-4's contract path cannot be known before dispatch for workflow, research and file-valued `--output` commands
Stated texts:
1. SPEC:62 (WC-4): "One report file, known before dispatch ... the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". It must be written "including stops before any other output exists". SPEC:73: the brief states "the output directory, so the report path is known before dispatch".
2. SPEC:92 (workflow, ready): brief passes `--handoff none` only; Report today `.dev/tasks/to-do/<id>/return-contract.yaml`; P1 fix "Write the contract for pre-creation STOPs too". `<id>` is generated by the command (INV-B:272: "Not written for pre-creation STOPs"); no directory is passed.
3. SPEC:90 (tdd): brief passes `--output <file>`; report is "the TDD at `--output`". SPEC:200 (AC-2.2) runs `/sc:tdd "auth" --unattended --output <file>` and expects "contract `status: blocked`". A file path is not a directory.
4. SPEC:116 (research): report "contract naming the generated `claudedocs/research_*.md` path"; no output flag, no directory.
5. SPEC:183 (7.2 step 4): `test -s <contract>` and the YAML check, on "the WC-4 contract path" named in SPEC:182 (step 3).
Grading check: An implementer who follows the stated text as written builds a coordinator brief and a 7.2 check for `workflow`, `research` and `tdd` in which `<output-dir>` is undefined: for workflow the directory is created by the command after the brief is sent; for research no directory exists; for tdd the passed value is a file. The coordinator then cannot compute the contract path before dispatch, WC-4's "known before dispatch" fails, and a pre-creation workflow STOP has no directory to hold the contract. Step 4 of the acceptance procedure and AC-1.4 (SPEC:198) cannot be evaluated.
Corroboration outside the workspace: `CMD:460` and `CMD:23` show the real spec-panel avoiding exactly this clash by adding a separate directory flag, `--report-dir`, because "`--output` is file-valued". That text also shows SPEC:120 ("add `--output`") and INV-B:43 (no `--output` exists) are stale against the current command definition.

=== ARCHITECTURE ANALYSIS ===

No further blocking finding. Notes below are Medium or minor and never fail the review.

Fowler: the split (one shared core file plus a short per-command section, SPEC:52) is sound and keeps the "no Orca calls in commands" rule checkable (SA-2, SPEC:147). The partition of 43 commands is consistent with both inventories.
Newman: the contract has no schema version, although the existing workflow contract is versioned ("contract 1.1", INV-B:272). WC-4 (SPEC:62) lists fields but no `contract_version`, so a later field addition cannot be detected by a coordinator (Medium, see FC-7).
Hohpe: the pull model (WC-12, SPEC:70; CAPS:66-67) and exactly-once `worker_done` (WC-5, SPEC:63) are correctly bounded by the Orca facts.
Nygard: failure paths are partly covered (WC-3 ask timeout, WC-6 retry, WC-10 liveness). Missing: behaviour when `~/.claude/WORKER-CONTRACT.md` is absent for a command whose section points to it (older install, plugin install; SPEC:279 admits the plugin mirror rule is unread) (Medium, FC-9).
Rejected-alternative argument (SPEC:29-39): R1-R5 hold against CAPS:97-103, 145-150. R1 correctly marks the enforcement call sites UNVERIFIED (CAPS:103).

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Findings use the FR-3 template. All are Medium (a requirement the text never states, or a reading needing an extra guess), so they sit under follow-up candidates.

- W1. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 and Decisions (SPEC:63, 263)** fails when **a command reports `status: partial` while having written none or one of its several artifacts**. Concrete attack: a `cleanup-audit` run with 12 batch reports planned writes 2 and hits a tool failure; it labels itself `partial` (WC-4 gives no definition of `partial`, SPEC:62); the worker sends `--outcome succeeded`; Orca settles the Task as completed (CAPS:77) and unblocks dependents (CAPS:90); the dependent `/sc:adversarial` worker reads 2 of 12 inputs. Before: Task dependents blocked. After: dependents ready.
- W2. I can break this specification by **Sequence Attack**. The invariant at **WC-3 and WC-4 (SPEC:61-62)** ("written on every outcome") fails when **the command's second run, started after a `blocked` contract and an `ask` answer, dies without writing**. Concrete attack: run 1 writes `status: blocked`; worker asks and gets an answer; run 2 is killed by context exhaustion before its write; the stale `blocked` file remains; WC-5 covers only "no report exists" (SPEC:63), so the stale file decides the outcome and the answered question is lost.
- W3. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-2/WC-4 (SPEC:60, 62)** fails when **`--unattended` is passed with no output directory or flag**. Concrete attack: `/sc:analyze src/x.py --unattended`; WC-4 says the contract goes to the passed directory, none was passed, and the command (SPEC:99) has no rule: it may write to the cwd (colliding with another worker, WC-11, SPEC:69) or refuse with no contract (violating "every outcome").
- W4. I can break this specification by **Divergence Attack**. The invariant at **WC-2 (SPEC:60)** (three resolutions only: default, caller flag, blocked) fails at **rows that say "refused under `--unattended`"** (SPEC:102, 103, 108, 110, 114, 123). Concrete attack: `/sc:test --watch --unattended`; "refused" is none of (a), (b), (c); the spec does not say whether a `blocked` contract is written, nor which Orca outcome follows.

=== GUARD CONDITION BOUNDARY TABLE ===
(Triggered: the candidate has guards, thresholds and sentinel comparisons. Nygard built it, Crispin checked completeness, Whittaker attacked entries. Classes left out are listed with a reason after the table.)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome map | SPEC:63 | Zero/Empty | no report file | no report -> failed | `--outcome failed` ("or no report exists") | OK |
| WC-5 outcome map | SPEC:63 | One/Minimal | `status: partial`, zero deliverables | partial -> succeeded | succeeded; no definition of `partial` (W1) | GAP (Medium: names no wrong outcome without an extra assumption about what a command labels partial) |
| WC-5 outcome map | SPEC:63 | Typical | `status: succeeded` | true | succeeded | OK |
| WC-5 outcome map | SPEC:63 | Sentinel Value Match | `status` outside the four-value set (existing vocabularies, SPEC:62 "keep their fields") | undefined | unspecified | GAP (Medium, FC-4) |
| WC-5 outcome map | SPEC:63 | Legitimate Edge Case | audit verdict FAIL with status succeeded | true | succeeded, body states verdict | OK |
| WC-2 unattended gate | SPEC:60 | Typical | gate with documented default | true | default applies | OK |
| WC-2 unattended gate | SPEC:60 | Legitimate Edge Case | "refused under `--unattended`" rows | n/a | unspecified (W4) | GAP (Medium) |
| WC-4 report location | SPEC:62 | Zero/Empty | `--unattended`, no output dir | unspecified | unspecified (W3) | GAP (Medium) |
| WC-4 report location | SPEC:62 | Legitimate Edge Case | generated id, file-valued `--output`, no flag | path unknown | contradiction, see F3 | GAP (BLOCKING, F3) |
| WC-10 wait split | SPEC:68 | Typical | poll iteration under 4 min | true | split into waits of at most 4 min | OK (poll runtime UNVERIFIED, SPEC:283) |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | one Agent-tool call (subagent wave) over 5 min | true | unspecified: Agent-tool waits cannot be split (FC-2) | GAP (Medium) |
| Depth fence | SPEC:33, 66 | Typical | depth 1, worker calls `worker-start` | refused | `nested_worker_depth_exceeded`, WC-8 forbids | OK |
| Depth fence | SPEC:33, 252 | Legitimate Edge Case | depth raised (D5 b) | not refused | out of scope, recommended against | OK |
| ask timeout | SPEC:61 | Typical | `ask` times out | true | resume same message ID, no duplicate | OK |
| task confidence | SPEC:121 | Legitimate Edge Case | confidence below 0.70 | true | blocked | OK (exactly 0.70 is outside "below"; INV-B:199 uses "< 0.70") |
| Heartbeat | SPEC:68 | Zero/Empty | no tool call blocks over 5 min | false | no split needed | OK |

Classes left out, with reason: Maximum/Overflow for WC-5, WC-2, ask and depth (no count or capacity enters those guards); One/Minimal and Sentinel for the depth fence (the setting is a single integer with a stated default; Orca falls back to 1 on a malformed value, CAPS:100); Sentinel Match for WC-10 (no sentinel value).
FR-8 GAP rows: F3 is blocking (it names a wrong outcome); the others are Medium warnings (follow-up candidates). FR-9 blank behaviors: the two "unspecified" rows above, graded Medium. FR-10: every guard is enumerated and every input class has a row or a stated omission.
