review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

- mode: critique; focus: requirements, architecture; whole-document audit, a first review (no `--re-review`, no `--baseline`; `baseline: missing` does not apply, none was requested)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `e588d816f4ebe8cc73b0f945a07b3aaec6c6e366428b45f3edd87fcc2d7056f5`
- baseline sha256: none given
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 27-32), including its grading check
- brief clauses overridden: none
- evidence class: the only checkable evidence is the README, the three inventories and `command.md` (the command definition). Spec = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Any `cmd/`, `sk/`, `CLAUDE.md`, `EVIDENCE.md`, `install_core.py` or `pyproject.toml` citation is UNVERIFIED unless an inventory line quotes it. I confirmed the spec's `INV-A:N`, `INV-B:N` and `CAPS:N` line citations against the three inventories (about 60 spot checks, spec lines 21-69 and 83-137); every one resolved to the claimed content. The spec's own "about 340 citations re-read" claim (spec:285) is UNVERIFIED.

## What I covered

All 285 lines of the spec: sections 1 (decision, evidence, rejected alternative, evidence strength), 2 (WC-1..WC-12, coordinator duties), 3 (43 per-command rows: counts reconcile to 10 + 27 + 6, and the phase assignment of every row reconciles with spec:158-162), 4, 5 (SA-1..SA-6), 6, 7 (AC-C1..C5, live check, per-phase checks), 8, 9 (D1..D5), Decisions, UNVERIFIED list. Counts checked: ready 5 + 5 (INV-A:73, INV-B:278), needs-change 13 + 14 (INV-A:73, INV-B:278), coordinator-only 3 + 3. Panel order followed: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower; findings are grouped by bucket below. Not covered: the content of any `cmd/`, `sk/` or repo file the inventories do not quote.

## Findings table (ids are stable for any re-review)

| id | severity (label) | graded | bucket | expert | spec location |
|---|---|---|---|---|---|
| F-01 | MAJOR | blocking | requirements | Wiegers, Adzic | spec:105, spec:201, spec:60 |
| F-02 | MAJOR | blocking | architecture | Fowler, Hohpe | spec:120, spec:62, spec:73, spec:160 |
| M-01 | MAJOR | Medium | requirements | Wiegers | spec:73, spec:79-92, spec:159, spec:195 |
| M-02 | MAJOR | Medium | requirements | Cockburn | spec:61, spec:218, spec:235 |
| M-03 | MAJOR | Medium | requirements | Crispin | spec:147, spec:150, spec:158, spec:172 |
| M-04 | MAJOR | Medium | requirements | Cockburn | spec:100, spec:121, spec:154, spec:160, spec:225, spec:244-247 |
| M-05 | MAJOR | Medium | architecture | Nygard, Whittaker | spec:62, spec:64, spec:85, spec:73 |
| M-06 | MAJOR | Medium | requirements | Crispin | spec:68, spec:210, spec:266 |
| M-07 | MINOR | Medium | architecture | Fowler | spec:92, spec:62, spec:73 |
| M-08 | MAJOR | Medium | architecture | Nygard | spec:63, spec:263; CAPS:90 |
| M-09 | MAJOR | Medium | architecture | Newman | spec:122; INV-B:209 |
| M-10 | MAJOR | Medium | requirements | Wiegers | spec:25, spec:76, spec:147, spec:172 (UNVERIFIED) |
| M-11 | MINOR | Medium | requirements | Hightower | spec:59 |
| M-12 | MAJOR | Medium | requirements | Adzic | spec:62, spec:183, spec:262 |
| M-13 | MINOR | Medium | requirements | Whittaker | spec:51, spec:228; command.md:459 |
| M-14 | MINOR | Medium | requirements | Gregory | spec:154, spec:225 |

## === REQUIREMENTS ANALYSIS ===

### F-01 (blocking, MAJOR, Wiegers/Adzic): cli-portify can never reach `succeeded` unattended, so AC-2.3 cannot pass for it
Grading sentence: an implementer who follows the stated text builds a cli-portify whose unattended run always ends `status: blocked` at the first approval gate, and that is wrong because spec:201 (AC-2.3) requires a happy-path run of every P2 command, with every required flag in the brief, to end `--outcome succeeded`, while the cli-portify row names no flag that supplies an approval.
- Text A, spec:105: "each of the three approval gates resolves as blocked"; the only other input is a new `--resume <contract>` that "uses the existing `resume_phase`/`resume_substep` fields". It does not say that resuming counts as approving the gate, or what the resumed run does at the gate it resumes from.
- Text B, spec:60 (WC-2): a gate resolves by a documented default, a caller-supplied flag, or blocked. The row picks "blocked" for all three and supplies no flag.
- Text C, spec:160 and spec:201: cli-portify is a P2 command, and P2 has AC-2.3 (happy path to `succeeded`). cli-portify is listed in P2 at spec:160 and its gates come from INV-A:45 (review after Phases 1 and 2, approval before Phase 3, final approval).
- The same three-gate structure is in the inventory (INV-A:45, INV-A:79), which proposed "route through ask or an explicit auto-approve flag"; the spec took neither.
- Recommendation: add to the cli-portify row either an explicit per-gate approval flag (or one flag naming the gates pre-approved by the person) or a statement that the happy path is three chained workers and AC-2.3 for cli-portify is the third. Priority High. Quality impact: Testability 5 to 8.

### M-01 (Medium): no phase gives `--unattended`, or the WC-4 contract, to several "ready" commands
- Spec:73 (section 2.3) says every brief carries "the exact command line including `--unattended`". Spec:76 says every changed command except `load` gains the `## Unattended mode` section, and spec:79 says the ready commands report "the named file until Phase 1 adds the contract".
- The "small fix" column gives brainstorm "None" (spec:84) and init-lite "None" (spec:87), and the P1 row (spec:159) lists only fixes to adversarial, cleanup-audit, index-repo, workflow. No phase adds `--unattended` or a WC-4 contract to brainstorm or init-lite. Spec:195 (AC-1.1) tests the commands "named in the P1 row", which is ambiguous for the four fix-only commands.
- Why Medium: it is a requirement the document does not state (which ready commands get the flag and section), not a text that does harm; the implementer picks between "all ready commands" and "only those listed".
- Recommendation: one sentence in section 6 naming which of the 10 ready commands get `## Unattended mode`, and in which phase.

### M-02 (Medium): WC-3 excludes the implement Ruling unconditionally, D2(b) would relay it
- Spec:61 (WC-3): the answer to an `ask` may supply only a value that no safety rule reserves, and "`implement`'s Ruling (D2(a))" is excluded. Spec:235 (D2 option b) relays the person's exact words through `ask` as the Ruling, and spec:218 (non-goal 6) says the rule is unchanged "unless the user chooses D2 option (b)".
- If the user picks (b), WC-3 as written still forbids it. A one-clause condition ("unless D2(b)") resolves it. Priority Medium.

### M-03 (Medium): AC-C1 can fail the compliant contract file
- Spec:147 (SA-2) permits a mention of Orca "inside the contract file"; spec:150 (SA-5) and spec:158 (P0) add an Orca section to `HOW-WE-WORK.md` and a brief template to `WORKER-CONTRACT.md`, all under `src/superclaude/core`.
- Spec:172 (AC-C1) greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and passes only on no output (excluding `ccsession-tag`). A contract file or routing section that names `orca orchestration ask`, as WC-3 and spec:180 invite, fails the check.
- Why Medium: an implementer can avoid the literal strings; the text does not force the failure. Recommendation: scope AC-C1 to `commands`, `skills` and `agents`, or exclude the two named core files.

### M-04 (Medium): P2 bakes in the D4 answer before D4 is decided
- Spec:154 says phases 1-3 need no user decision; spec:225 says phases 0-3 proceed "on the recommendations"; the two statements differ (see M-14).
- Spec:100 (auggie-review) makes posting return "with an explicit `--post-pr` in the brief", and spec:121 (task) keeps `commit`/`push` available "unless authorized"; both are P2 (spec:160). Spec:244-247 (D4) asks whether a brief may authorize outward actions at all, and its option (b) says "Never". If the user picks (b), the P2 text built the opposite.
- Recommendation: state in P2 that the explicit-flag path is built only as D4(a), or move those two flags to P4.

### M-06 (Medium): WC-10 and AC-4.3 disagree on the wait threshold
- Spec:68 (WC-10): split only a single call "longer than 5 minutes", into waits "of at most 4 minutes". Spec:210 (AC-4.3): "no single tool call exceeds 240 s". A 4.5 minute wait is allowed by the rule and fails the check. The rationale at spec:266 (4 minutes leaves margin) supports the stricter number as the rule.
- WC-10 also does not address a single long Agent-tool fan-out call (tdd, adversarial) that blocks the main session more than 5 minutes; whether Orca uses heartbeat age at all is UNVERIFIED (CAPS:130, CAPS:182), so a mandatory 5-minute heartbeat has an unknown effect.
- Recommendation: make the rule threshold 4 minutes everywhere, and state that fan-out calls are exempt or how they heartbeat.

### M-11 (Medium): WC-1 has no owner or phase
- Spec:59 assigns WC-1 (no prompt before the agent is ready) to "Launch setup, not commands". No phase in section 6 or check in section 7 covers launch setup, and the one launcher in scope is `ccsession-tag` (spec:25). The requirement is therefore stated and never delivered.

### M-12 (Medium): status vocabulary versus "keep their fields"; PyYAML
- Spec:62 says commands that already write a contract "keep their fields and add the missing ones", while spec:262 fixes the status vocabulary to `succeeded/partial/failed/blocked`, and spec:183 asserts that vocabulary for every contract. Whether the existing contracts (workflow, reflect, brainstorm, adversarial) already use these values is not shown in any inventory (INV-B:272 only says "status ... including failed"). If any uses another word, AC step 4 fails.
- Spec:183 relies on PyYAML as "a declared dependency, `pyproject.toml:38`" (UNVERIFIED); the project instructions list only pytest, click and rich as dependencies. Recommendation: say whether existing status words are mapped or replaced, and confirm the dependency or use a tool already installed.

### M-13 (Medium, Whittaker): the spec does not define how `--unattended` is recognised
- Spec:228 says the flag "cannot misfire on a person". It is silent on a quoted topic or argument that contains the string (for example a troubleshoot description quoting a command line), and on `--unattended` combined with `--interactive` for commands where only some rows refuse it (spec:103, 110, 118 refuse it; brainstorm, release-split, adversarial rely on the brief omitting it). `command.md:459` defines a rule for its own command (standalone token outside quoted arguments); the shared contract should state one rule for all. Sentinel collision attack: before state = quoted topic "why does --unattended fail"; after state = mode flips and prompts vanish for a person. Priority Medium.

### M-14 (Medium): contradictory statement of which phases need a decision
- Spec:154: "Phases 1-3 need no user decision". Spec:225: "Phases 0-3 can proceed on the recommendations". D1 (spec:227-230) must be settled before P1 writes any command section; the spec writes itself for the recommendation (spec:51) but does not say so in section 6.

## === ARCHITECTURE ANALYSIS ===

### F-02 (blocking, MAJOR, Fowler/Hohpe): the spec-panel row describes a command surface the supplied command definition no longer has, and WC-4's contract location conflicts with it
Grading sentence: an implementer who follows spec:120, WC-4 (spec:62) and P2 (spec:160) adds `--output` and `--unattended` to `/sc:spec-panel` and tells the coordinator the contract is at `<--output value>.return-contract.yaml`, and that is wrong because the command definition (`command.md:22-24`) already has `--output <file>`, `--unattended`, `--report-dir`, and writes `<report-dir>/return-contract.yaml` (`command.md:460-461`), refusing the run when `--report-dir` is missing (`command.md:460`).
- The spec's basis: spec:120 ("add `--output`; contract") and spec:62 ("Where `--output` is a file (tdd, init-lite, spec-panel), the contract is `<value of --output>.return-contract.yaml`"), from INV-B:182 ("no path or `--output` flag exists (:22)") and INV-B:185.
- Contradicting source: `command.md:22-23` (usage lists `--output <file>`, `--unattended`, `--report-dir <dir>`, `--improve`), `command.md:457-465` (an Unattended mode section that points to `~/.claude/WORKER-CONTRACT.md`, which the spec proposes to create in P0 at spec:52 and spec:158).
- Follow-on effects under the spec's own brief rule (spec:73): a brief that passes only `--output` gets a refusal printed in chat only (`command.md:460`), so no contract exists at the path WC-4 tells the coordinator to open, and AC-2.2 step 4 (spec:183, `test -s <contract>`) fails for a compliant worker. WC-4 has no rule that git-ignored paths are left out of `artifacts`, which `command.md:461` attributes to a WC-4 of the installed contract.
- Basis and limit: this holds if `command.md` is the repo's current spec-panel definition; the spec's own view of `cmd/spec-panel.md` is UNVERIFIED here. If `command.md` is current, the same staleness check is owed to every row whose basis is an inventory read dated 2026-11-02 (spec:11). Resolving evidence: diff the spec-panel row, WC-4 and the contract-location rule against the installed `WORKER-CONTRACT.md`, then decide one contract-location convention (`--report-dir` or `--output`-derived).
- Priority High. Quality impact: Consistency 4 to 8.

### M-05 (Medium, Nygard/Whittaker): retry and fresh-directory rule leaves a stale contract readable
- Spec:64 (WC-6): a command without a resume flag "writes each run into a fresh output directory". Spec:62 (WC-4) fixes the contract path in the brief before dispatch, and spec:73 does not tell the coordinator to pass a new directory per retry. Spec:85 notes cleanup-audit's output directory is fixed, so a retry shares it.
- Sequence attack: attempt 1 writes `return-contract.yaml` with `status: failed` into `<dir>`; the retry (`--retry-of`) gets the same brief and `<dir>`, is killed before writing; the coordinator opens `<dir>/return-contract.yaml` and reads attempt 1's report as the retry's result. A retry that only blocks on a gate never trips Orca's circuit breaker, because a worker's own failed report does not count (CAPS:80). Recommendation: add to section 2.3 that a retry brief names a new output directory and that the coordinator removes or ignores a contract older than the dispatch.

### M-07 (Medium): workflow contract location is not known before dispatch
- Spec:92 (workflow) puts the contract at `.dev/tasks/to-do/<id>/return-contract.yaml` and asks to "write the contract for pre-creation STOPs too". The `<id>` is created at run time (INV-B:272), and no output directory is in the brief (spec:92 "Brief must pass: `--handoff none`"), so spec:62 and spec:73 ("path known before dispatch") do not hold, and for a pre-creation stop there is no package directory to hold it. State where that contract goes.

### M-08 (Medium, Nygard): `partial` maps to `succeeded`, which unlocks dependent Tasks
- Spec:63 and spec:263 map `partial` to `--outcome succeeded`. Orca keeps dependents of a failed Task blocked and runs those of a completed one (CAPS:90). WC-4 defines `partial` without the condition spec:263 gives (a "usable deliverable"), so a command can report `partial` for any shortfall and release downstream Tasks. Recommendation: define `partial` as "deliverable present and usable", and say the coordinator's `--deps` waves treat other cases as failed.

### M-09 (Medium, Newman): tasklist row leaves two nested gates unresolved
- Spec:122 resolves only Stage 10.5 (pass `--unattended` to each reflect). INV-B:209 shows `needs_human_decision` items in that stage HALT, and spec:122 does not say how a HALT resolves under WC-2. INV-B:211 also shows Stage 9 calls `sc:task --compliance strict`, whose confidence gate is resolved only for a direct `sc:task` run (spec:121), not for this nested call. Spec:122 also assumes the nested spawning depth is safe by citing INV-A:14, while INV-B:314 and INV-B:322 list the same question as UNVERIFIED; the two inventories disagree and the spec does not say which it relies on.

### M-10 (Medium, UNVERIFIED): scope and baseline claims are not checkable and may be stale
- Spec:76 fixes the scope at 43 commands; spec:25 (E5) and spec:147 (SA-2) rest on "no command, skill, agent or core file calls Orca today", from a grep not repeatable here. The session's installed skill list names `sc:graph`, `sc:impact` and `sc:issue`, which neither inventory covers, and `sc:issue` is described as creating an Orca worktree and launching an agent. I cannot cite a file for this (it is outside the sandbox), so it is UNVERIFIED.
- If true, E5, SA-2 and the baseline of AC-C1 (spec:172) are wrong, and the 43-command count is incomplete. Resolving evidence: re-run the E5 grep and list `src/superclaude/commands/` on the current branch.

## Guard Condition Boundary Table

Trigger: yes (thresholds, boolean switches and sentinels throughout). Guards with a numeric or boolean condition in the spec: G1 `--unattended` switch, G2 WC-5 outcome mapping, G3 WC-10 wait/heartbeat, G4 output-path presence (WC-4), G5 WC-6 retry, G6 confidence `<0.70` (task row). Classes left out: Maximum/Overflow for G1, G2, G4 (no capacity concept; the guard is boolean or an enumeration).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` | spec:60, spec:146 | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1) | OK |
| G1 | spec:60 | One/Minimal | flag present, no other flag | true | gates resolve per row | OK |
| G1 | spec:228 | Sentinel Value Match | string `--unattended` inside a quoted argument | true or false | not specified (M-13) | GAP |
| G1 | spec:103, 110, 118 | Legitimate Edge Case | `--unattended` with `--interactive` | true | refused for cleanup, improve, roadmap only; others silent | GAP |
| G2 outcome mapping | spec:63 | Zero/Empty | no report file | n/a | `--outcome failed` | OK |
| G2 | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G2 | spec:63, 263 | Legitimate Edge Case | `status: partial` with no usable deliverable | true | maps to succeeded (M-08) | GAP |
| G2 | spec:63 | Sentinel Value Match | report exists, `status` missing or outside the four values | n/a | not specified | GAP |
| G3 wait/heartbeat | spec:68, 210 | Maximum/Overflow | single call of 4.5 min | rule: no split; AC-4.3: fail | rule and check disagree (M-06) | GAP |
| G3 | spec:68 | Typical | wait of 3 min | n/a | allowed | OK |
| G4 output path | spec:62, 73 | Zero/Empty | `--output` omitted under `--unattended` | n/a | not specified in the spec; `command.md:460` refuses | GAP |
| G4 | spec:62 | Legitimate Edge Case | `--output` is a file (tdd, init-lite, spec-panel) | n/a | `<value>.return-contract.yaml` (conflicts with F-02) | GAP |
| G5 retry | spec:64 | Maximum/Overflow | N retries all ending `blocked` | n/a | circuit breaker does not count blocked reports (CAPS:80); not addressed | GAP |
| G5 | spec:64 | Legitimate Edge Case | retry reuses the brief's output directory | n/a | stale contract readable (M-05) | GAP |
| G6 confidence | spec:121 | Typical | 0.50 | true | blocked | OK |
| G6 | spec:121 | Legitimate Edge Case | exactly 0.70 | false | "below 0.70" blocked; 0.70 proceeds | OK |

Every GAP is graded in the findings above: those that name a concrete wrong outcome an implementer would produce are F-01 and F-02; the rest are Medium (FR-8/FR-9 graded by consequence). The table is complete for the enumerated guards, so the FR-10 gate is satisfied for synthesis.

Pipeline Dimensional Analysis: not triggered. The spec has a phase sequence and a Task fan-out, but no data flow whose item count changes between stages that downstream consumers assume to be conserved. Quantity Flow Diagram: not produced.

## Notes (minor, never failing)

- N-1: spec:22 cites `EVIDENCE.md:45` for "answered"; CAPS:49 quotes only "state: ready, stage: input_accepted" and does not mention an answer. EVIDENCE.md itself is UNVERIFIED here.
- N-2: spec:285 lists an independent citation check as an "UNVERIFIED item" although it is a statement of work done; it cannot be checked from the sandbox.
- N-3: spec:122 and spec:104 use "one layer below the worker" and "waits of at most 4 minutes" as if stated by Orca or Claude Code; both are the spec's own design choices (spec:266) or an inventory reading (INV-A:14).
- N-4: AC-1.3 (spec:197) tests the standalone run with `claude -p`; reflect's headless rule keys on `--print` (INV-B:109), so for reflect the test is not a plain-session test.

## Follow-up candidates (Medium and minor; none triggers a revision)

M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-09, M-10, M-11, M-12, M-13, M-14, and notes N-1 to N-4. The session asking the user once per loop whether to open an issue for these was not possible in this run, because the brief restricts the final reply to the output path; no issue was created and none is implied. Recorded for the coordinator to ask.

## Consensus and disagreement

- Consensus: the decision (section 1), the evidence statement of gaps (section 1.4) and the reconciliation of counts and phases are sound; the inventory citations resolve.
- Disagreement: Wiegers and Adzic treat F-01 as blocking (a stated acceptance check cannot pass); Fowler wanted M-05 blocking, held to Medium because the coordinator can notice a stale file (it needs an assumption about coordinator behaviour). Whittaker's M-13 and the G1 sentinel rows stay Medium for the same reason.

## Reviser brief

Blocking finding ids: F-01, F-02. Reviser contract (restated from `/sc:spec-panel` Review Loop bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award a PASS. F-01 names spec:105 and spec:201; F-02 names spec:62, spec:120 and spec:160.

verdict: FAIL
