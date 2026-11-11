review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `2fadf1465791032cab449691f98fc1d6c0b5bd279da252336d54f84f58e6198f`
- baseline: none given; `--re-review` not given. This is a first review of the full document, a labelled whole-document audit, not a re-review.
- baseline sha256: n/a
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- mode: critique; focus: requirements, architecture (no `--focus correctness`, so no State Variable Registry)
- citation key: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Binding context: `README.md:1-39`.
- coverage line: whole-document review of all sections 1-9, Decisions and UNVERIFIED; every `INV-A:`, `INV-B:` and `CAPS:` citation in sections 1-4 was spot-checked against the three inventory files (about 60 line citations, no wrong line found). Citations to `src/`, `CLAUDE.md`, Orca compiled files, `EVIDENCE.md`, `.dev/codegraph-migration/...` and installed `~/.claude` files are UNVERIFIED here unless an inventory line quotes them, because they are outside the workspace.

## Result in one paragraph

No blocking finding. The 10 / 27 / 6 partition is arithmetically and textually consistent with the inventories (3.1 has 10 rows, 3.2 has 27, section 4 has 6, total 43; the phase lists in `spec:159-162` cover exactly those 37 plus load). The core decision (spec:16-39) is supported by the Orca facts as quoted (`CAPS:97-103`, `CAPS:147-150`). There are 15 Medium findings (F1 to F15): requirements the document never states or states two ways, none of which makes the stated text itself cause a wrong build. Under the grading check, each needs the implementer to guess.

## Grading rule applied

Blocking only if "an implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (contradiction, data loss or safety-boundary break, or an acceptance criterion that cannot pass). Findings that need a guess, or are a requirement the document never states, are Medium and listed under `follow-up candidates`. (`document_review_loop_prompts.md:31`)

## Blocking findings

None.

## Guard Condition Boundary Table

Trigger: the spec contains threshold checks, boolean switches and sentinel comparisons (60 s readiness, 4 min vs 5 min wait, `--unattended`, status values, 0.70 confidence, depth 1). Constructed by Nygard, completeness by Crispin, attacked by Whittaker. Status GAP rows are graded under FR-8 (all Medium; none names a concrete wrong outcome without a guess).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` switch | spec:51, 60, 228 | Zero/Empty | flag absent | false | today's behaviour unchanged (spec:146, SA-1) | OK |
| G1 | spec:51, 228 | Typical | flag + output dir passed by coordinator | true | WC-2 gates resolve, contract written (spec:60, 62) | OK |
| G1 | spec:228 | Sentinel Value Match | the token `--unattended` inside a quoted free-text argument, e.g. `/sc:tdd "add --unattended mode"` | ambiguous | not stated; the spec says only "cannot misfire on a person" | GAP (F2) |
| G1 | spec:62, 159 | Legitimate Edge Case | `--unattended` with no output directory | true | not stated (no refusal rule, no default) | GAP (F1) |
| G2 WC-5 outcome mapping | spec:63 | Zero/Empty | contract missing, empty or unparseable | n/a | `--outcome failed`, body says contract invalid | OK |
| G2 | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G2 | spec:62, 63, 183 | Sentinel Value Match | existing contract whose `status` uses another word | outside the four values | WC-4 "keep their fields" vs WC-5 "outside the four values => failed" vs AC step 4 assert | GAP (F7) |
| G2 | spec:63, 263 | Legitimate Edge Case | `status: partial` | true | maps to succeeded; what counts as partial is not defined per command | GAP (F4) |
| G3 WC-10 wait split | spec:68 | Typical | tool call under 4 min | false | worker heartbeats between calls | OK |
| G3 | spec:68, 104 | Maximum/Overflow | cli-eval eval up to 3600 s | true | split into waits of at most 4 min | OK |
| G3 | spec:68 | Legitimate Edge Case | one blocking Agent-tool (Task) call longer than 5 min | not covered | WC-10 names only a "single tool call" for poll waits and long evals; fan-out waves are not addressed | GAP (F5) |
| G4 nesting depth (WC-8, R1) | spec:33, 66 | Typical | depth 1, command calls `worker-start` | true | refused (`CAPS:97-101`) and WC-8 forbids the call | OK |
| G4 | spec:252 | Legitimate Edge Case | depth raised (D5 b) | false | WC-8 still forbids the call; R1 no longer a reason | OK |
| G5 task confidence | spec:121 | Typical | 0.50 | true | blocked | OK |
| G5 | spec:121 | One/Minimal edge | exactly 0.70 | false | the row says "below 0.70" (matches `INV-B:199`) so 0.70 proceeds | OK |
| G6 WC-9 outward default-off | spec:67 | Typical | no authorization in brief | true | off | OK |
| G6 | spec:67, 100, 113, 121 | Legitimate Edge Case | brief authorizes an action | depends on a flag | auggie-review `--post-pr`, post-release and task authorization flags are not evidenced as existing and not defined | GAP (F6) |
| G7 readiness (WC-1) | spec:59 | Maximum/Overflow | wrapper prompt fallback above about 45 s | true | fails again (`EVIDENCE.md:56` via `CAPS:49`) | OK |
| G7 | spec:59 | Legitimate Edge Case | "well inside" the limit | undefined | no numeric bound given | OK as note (M3) |

Classes left out: Zero/Empty and Maximum for G3-G5 and G7 cannot occur for those guards (G4 depth is a setting at 1 or more, `CAPS:100`; G5 is a bounded confidence value; G7 has no empty input). G1 and G2 Maximum cannot occur (boolean, closed enumeration, except as listed). G3 Sentinel: no sentinel value exists in a duration. G4/G5/G6 Sentinel: no magic constant is compared.

No GAP row is blocking (FR-8): each needs a guess about what the implementer does.

## Pipeline Dimensional Analysis

Not triggered as a data pipeline (no multi-stage data flow with N != M). The only count-conservation check that applies is the command partition: 21 + 22 = 43 commands (`INV-A:3`, `INV-B:3`); 10 + 27 + 6 = 43 (`spec:76`, 3.1 rows `spec:83-92`, 3.2 rows `spec:99-125`, section 4 rows `spec:132-137`). Phase lists: P1 15, P2 15, P3 4, P4 3 = 37 = 10 + 27 (load included in P1 by its usage-line fix, `spec:112, 159`). Conserved. No Quantity Flow Diagram needed.

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### F1. Contract location undefined where no directory-valued output flag exists (Medium, High priority, Wiegers)
- Stated: WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). P1 adds "output flags for commands that lack one" (spec:159). AC-1.2 runs each P1 command with `--unattended --output <dir>`, with `init-lite` the only carve-out (spec:196, N-2 at spec:87).
- Gap: the 3.1 rows for cleanup-audit ("output dir is fixed", spec:85), index-repo ("Brief must pass: none", "State the output location", spec:86) and tdd (`--output <file>`, spec:90) name no directory flag and no contract location. For tdd, `--output` is a file, so `<output-dir>` has two readings (the file, or its parent). Under the parent reading, two TDD workers writing `docs/x/TDD_A.md` and `docs/x/TDD_B.md` share `docs/x/return-contract.yaml`, which WC-11 forbids (spec:69). The 3.2 rows "add `--output`" (spec:99, 106, 107, 111, 120, 123) also do not say file or directory, while init-lite needed a separate `--output-dir` for exactly this reason (spec:87). Evidence of the inventory side: `INV-A:42, 53, 55`; `INV-B:47`.
- Why Medium: the build depends on which reading the implementer picks.
- Recommendation: state one rule (a `--output-dir` for every command whose `--output` is file-valued or absent) and list it per command in 3.1. Priority High.

### F2. How `--unattended` is recognised is not specified (Medium, Medium priority, Adzic)
- Stated: D1(a) says the flag "is testable by grep and cannot misfire on a person" (spec:228). Free-text commands take quoted prompts: tdd topic (spec:90), troubleshoot symptom (spec:194), recommend, spec-panel specification content (INV-B:43).
- Attack (Whittaker, Sentinel Collision): the token appearing inside quoted content, or inside a file the command reads. The spec has no "standalone argument outside quotes" rule. A hit would silently turn off gates for a person (breaking SA-1, spec:146) or hide the flag from a worker.
- Recommendation: add one sentence to the contract-file scope in 2.1 (spec:51-52) fixing the recognition rule.

### F4. `partial` is mapped to `succeeded` with no per-command definition (Medium, Medium, Wiegers/Whittaker)
- Stated: `partial` -> `--outcome succeeded` (spec:63, spec:263). Orca keeps dependents of a failed Task blocked (`CAPS:90`), so a `succeeded` partial unlocks dependent Tasks.
- Gap: nothing says when a command may report `partial` (cleanup-audit with 2 of 3 passes, implement with some tasks skipped, cli-portify mid-phase). The 3.x rows never use the word. An implementer may mark any incomplete run `partial` and let dependents run on incomplete output. The body's first sentence says `partial` (spec:63), which a coordinator reads only if it looks.
- Recommendation: define `partial` per command in one clause, or add a `dependents_may_proceed` field.

### F6. WC-9 relies on authorization flags that are not evidenced or defined (Medium, High, Wiegers)
- Stated: outward actions turn on "only through the command's own explicit flag written in the brief" (spec:67). The auggie-review row says posting "returns only with an explicit `--post-pr` in the brief" while "Other required change: none" (spec:100). `INV-A:38` and `INV-A:78` show only `--no-post-pr` and `--no-remediation-offer`; no `--post-pr` appears in the inventory. The post-release row says "unless the brief authorizes them" (spec:113) and the task row "refused unless authorized" (spec:121) with no flag named; AC-4.2 speaks of "no authorization flags" (spec:209). `INV-B:79, 204` show the real mechanisms are a session-level "pre-authorized" and keyword-triggered `commit`/`push`.
- Effect: the safe default (off) holds, but the on-path cannot be implemented as written. `--post-pr` is UNVERIFIED as an existing flag (cmd file outside workspace).
- Recommendation: name each flag and mark the new ones as additions in 3.2 "Other required change".

### F7. Existing contracts keep their fields, yet WC-5 and AC step 4 fix the status vocabulary (Medium, Medium, Wiegers)
- Stated: commands that already write a contract "keep their fields and add the missing ones" (spec:62); WC-5 sends any `status` outside the four values to `failed` (spec:63); AC step 4 asserts `status in {succeeded, partial, failed, blocked}` for every contract (spec:183). Workflow, reflect, brainstorm and adversarial already write contracts (spec:261; `INV-B:272`, `INV-B:112`, `INV-A:39`, `INV-A:35`). The inventories list their fields but not the value sets of `status` (`INV-B:272` names `status`, `plan_path`, `reflect_report_path`).
- Effect: if any existing `status` uses another word, "keep their fields" and the AC cannot both hold. Whether they do is UNVERIFIED (the contracts are outside the workspace).
- Recommendation: add the value check to P0 or P1 (compare each existing contract's value set with the four) before the AC is written.

### F3. Phase sequencing conflicts with its own "no user decision" claim and with AC-1.1 (Medium, Medium, Cockburn)
- Stated: P1 adds the `--unattended` flag to "every command in sections 3.1 and 3.2 except load (a no-op where a command has no gate)" (spec:159); gates convert in P2 (spec:160); P1 "needs no user decision", P4 waits for D2-D4 (spec:154). AC-1.1 requires every such command to carry a section "naming its report file" at P1 (spec:195).
- Gap 1: between P1 and P2/P4, a command that has a gate (auggie-review, cleanup, post-release) accepts `--unattended` but does not yet change behaviour; the parenthetical covers only commands "with no gate". The spec does not say a coordinator must not dispatch those commands until their phase passes.
- Gap 2: AC-1.1 needs a named report file for validate-roadmap (command and skill still disagree until P3, spec:124, 204), validate-tests (P3), implement, post-release and pr-submit (P4, D2-D4).
- Gap 3: D4 lists auggie-review `--post-pr` and task `commit`/`push` as affected by the decision (spec:244), yet both rows are P2 (spec:100, 121, 160), and P2 is described as "touches no safety rule and adds no outward capability" (spec:160) while the auggie-review row adds an on-path for posting.
- Why Medium: each needs the implementer or coordinator to act on the gap in a particular way.
- Recommendation: add one line to section 6 saying a command is dispatchable as a worker only after its own phase passes, and move the on-path of `--post-pr` and task commit/push to P4.

### F11. Several requirements have no acceptance check (Medium, Low, Crispin)
- WC-3 (ask / resume same ID, spec:61): AC-2.2 tests the blocked outcome (spec:200), never an `ask` / `reply` round trip.
- WC-12 (`check` before `worker_done`, `consumer_fenced`, spec:70): no AC.
- WC-7 (no Agent-tool wrapper, spec:65): checked only in P0 (spec:194), not for P1-P4 live runs.
- WC-11 (parallel-safe writes, spec:69): only `save` has a check (AC-3.4, spec:207); fixed paths such as `PROJECT_INDEX.md` (`INV-A:53`) and `.claude-audit/` (spec:85) have none.
- WC-10 for cli-eval (spec:104): the 4-minute split has no AC; AC-4.3 covers pr-submit only (spec:210).
- Recommendation: add the missing checks, or mark those requirements as untested by design.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)

### F5. Liveness rule covers poll waits but not Agent-tool waits (Medium, Medium, Nygard)
- Stated: the worker heartbeats every 5 minutes (spec:68); a step that blocks "a single tool call" longer than 5 minutes must be split into waits of at most 4 minutes. The listed causes are a poll wait and a long eval.
- Gap: a top-level session blocked on one Agent-tool call (a fan-out wave of 7-8 agents, `INV-A:42`; adversarial Mode B, `INV-A:35`; tdd with 6-10+ agents, `INV-B:221`) cannot heartbeat either, and those waves can exceed 5 minutes. The spec neither bounds them nor says heartbeats can be skipped. Whether Orca uses heartbeat age at all is UNVERIFIED (`CAPS:130`, `CAPS:182`), so the rule may be unnecessary, which the spec should then say instead of constraining wait sizes.
- Recommendation: either state that fan-out waves are exempt (the worker is live while a subagent runs) or state a bound.

### F8. Retry and fresh-directory mechanism is ambiguous (Medium, Medium, Hohpe)
- Stated: WC-6 says a command without a resume flag "writes each run into a fresh output directory" (spec:64); WC-4 says the report path is known before dispatch (spec:62, 73). Most 3.1 and 3.2 rows say "Fresh dir" (e.g. spec:88, 91, 99-107).
- Reading A: the coordinator passes a new `--output` dir for each retry (not stated in 2.3, spec:72-73). Reading B: the command creates a new subdirectory under the passed dir, so the contract is not at `<output-dir>/return-contract.yaml`, which is what the AC reads (spec:182-183). Under the same dir with no fresh dir, a `--retry-of` worker overwrites attempt 1 while attempt 1 may still be alive, because Orca reports `unverifiable` rather than dead (`CAPS:122-125`).
- Recommendation: add "on a retry the coordinator passes a new output directory" to 2.3.

### F9. tasklist Stage 10.5 resolution leans on unverified assumptions and skips a stop (Medium, Medium, Fowler)
- Stated: under `--unattended`, Stage 10.5 passes `--unattended` to each reflect so "the headless rule applies" (spec:122), and the fan-out is "one layer below the worker, inside Claude Code's nesting limit" (spec:122).
- Gaps: (1) The headless rule keys on `claude --print`; the spec's own UNVERIFIED item 9 assumes an Orca worker is not headless (spec:280; `INV-B:310`). (2) The inventory says Stage 10.5 also HALTs on `needs_human_decision` items (`INV-B:209`); the row does not say how that HALT resolves under WC-2. (3) `INV-B:215` recommended running the reflect fan-out at the worker's top level, and `INV-B:210` marks nested spawning UNVERIFIED; the spec rejects both without a reason. Layer count: worker -> reflect subagent -> its reviewers -> adversarial advocates is more than "one layer".
- Recommendation: add the `needs_human_decision` resolution and a depth note, or adopt `INV-B:215`.

### F10. pr-submit row omits its own "Will Not" and the escalation message (Medium, Low, Newman)
- `INV-B:90` records that pr-submit says "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`) and is an attended loop. The 3.2 row (spec:114) and D3(b) (spec:241) apply wait splitting and HALT-as-blocked but do not say the Will Not is lifted. D3(a) is recommended, so this affects only the (b) path.
- The row says the worker "may use `ask` or `escalation`" (spec:114) while WC-7 lists lifecycle messages as `heartbeat`, `ask`, `check`, `worker_done` (spec:65). `escalation` is a valid type (`CAPS:75`), so the list is incomplete.

### F13. No coordinator-side rule for a stalled or repeatedly blocked worker (Medium, Low, Nygard)
- The spec says a silent stall is "invisible" except through `worker-show` or a missing report (spec:44) and gives a 5-minute `worker-show` cadence in the AC (spec:181). Section 2.3 (spec:72-73) states what the coordinator owes the worker, not what it does when no `worker_done` arrives or when a Task keeps resolving `blocked` (each blocked run is a `failed` Task, `CAPS:90`; a worker's own `failed` report does not trip the circuit breaker, `CAPS:80`). There is no retry cap for blocked runs and no rule on how long to wait. `CAPS:126` says silence never authorizes stop or release, which the spec could cite.
- Recommendation: one paragraph in 2.3.

### F14. SA-2 allows an Orca mention that AC-C1 would reject (Medium, Low, Fowler)
- SA-2: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file" (spec:147). The contract file lives in `src/superclaude/core/` (spec:52). AC-C1 greps `src/superclaude/core` for `orca(-ide) (orchestration|worktree|terminal|agent)` and must print nothing (spec:172), excluding only `ccsession-tag`. P0 also adds an Orca section to `HOW-WE-WORK.md` (spec:158, 150). A natural example, "`orca orchestration ask`", matches the pattern. Whether a collision happens depends on wording, hence Medium.
- Recommendation: exclude the two named files from AC-C1 or forbid the command-shaped wording in SA-2.

### F15. Unattended destructive edits have no recovery requirement (Medium, Medium, Nygard)
- cleanup and improve apply non-approval items unattended and list the rest (spec:103, 110); their "rollback" claims are UNVERIFIED (`INV-A:43`, `INV-A:52`, `INV-A:118`); the spec requires the report to list every changed file but no snapshot or check. WC-9 covers outward actions only (spec:67). Two workers in one worktree (spec:69) can then both edit the same files. The effect depends on repository state, so Medium.
- Recommendation: require a clean working tree or a recorded start sha before an unattended cleanup/improve, as implement already does (`INV-A:51`, ledger start sha).

## === SCOPE AND EVIDENCE NOTES ===

### F12. The 43-command count rests on the inventories' scope lines (Medium, Low, Wiegers)
- The spec says "The 43 commands in `cmd/`" (spec:76); the evidence is two scope lists (`INV-A:3`, `INV-B:3`), not a directory listing. The reviewer's session skill list also names `sc:graph`, `sc:impact` and `sc:issue`, none of which appear in either inventory; `sc:issue` is described there as creating an Orca worktree and launching an agent, which would conflict with E5 and AC-C1 if present in `src/superclaude/commands/` (spec:25, 172). UNVERIFIED: this comes from the session environment, not from a file in the workspace, and the repo state at that time is not known.
- Recommendation: add a P0 step comparing the directory listing with the 43 names, and re-check E5.

## Verification notes

- Spot-check results that matched: `INV-A:35-55` and `INV-B:31-52` are the per-command rows (spec:24); `INV-A:76-83`, `INV-A:94-98`, `INV-B:289-299` are the gap tables (spec:26); `INV-A:106`, `INV-B:320`, `INV-B:323` are the check and "not run end to end" lines (spec:11, 43); `INV-A:113`, `INV-A:120`, `INV-A:118` (spec:277-278, 220) match; `CAPS:97-103`, `CAPS:147-150`, `CAPS:52`, `CAPS:129`, `CAPS:155-161`, `CAPS:178-188` match their claims.
- E5's grep results (`spec:25`) and the claims about `install_core.py`, `CLAUDE.md:74, 83, 334, 408`, `cmd/pr-submit.md:49` and `SKILL.md:46-64` are UNVERIFIED here. For pr-submit, `INV-B:95` states the wait as "up to --timeout 600 s per wait over several rounds" and asks for heartbeats; the spec's re-reading (spec:68, 114) that it is already iterated cannot be checked.
- The disposition and earlier review (`review/spec-panel.md`, `review/disposition.md`, `README.md:23-24`) are not in the workspace.

## Minor notes (never fail the review)

- M1. Revision labels R-1 to R-5, N-1 and N-2 appear in the text (spec:61, 62, 63, 64, 87, 159, 229, 234, 245) with no key in the document; a reader of the final spec cannot resolve them.
- M2. 2.1 says unattended mode is "the only command-side change the contract asks for besides report files and resume" (spec:51); section 3 adds tool changes, drift fixes and wait splitting (spec:108, 118, 124, 125, 104), later covered by SA-4 (spec:149). Reword 2.1.
- M3. WC-1 "well inside the readiness limit" (spec:59) has no number; the evidence gives 30 s passing and about 45 s failing (`CAPS:49`).
- M4. AC-C5 (spec:176) flags any removed line, but a new flag in an existing Usage line is a changed line; say flags are added on new lines or exempt Usage lines.
- M5. Reflect's tracked write `docs/memory/reflect/deviation-patterns-<slug>.md` and default folder move (`INV-B:114`) are not in WC-11 or the reflect row (spec:88); `--no-promote` covers only the move.
- M6. roadmap writes memory through `sc:save` every wave (`INV-B:154`); the roadmap row (spec:118) does not say the nested save runs in unattended mode, while WC-11 forbids single-owner keys (spec:69, 119).
- M7. workflow's `.dev/tasks/` staging rule (`INV-B:274`, UNVERIFIED whether `git add` runs) is not covered by WC-9, which lists push, PR, post, install and paid runs only (spec:67).

## Follow-up candidates

Medium: F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15.
Minor: M1 to M7.

Issue creation: the session that ran this review would ask the user once whether to open an issue for these; this is an attended-style audit run by a worker with no user channel, so the list is only recorded here and no issue was created.

## Reviser brief

None. No blocking finding is open, so no reviser pass is requested. (A brief may not widen scope to Medium or minor findings; see command Review Loop bullets 6 and 7. No brief clause was overridden: the coordinator's brief asked for a whole-document first review and nothing in it widened the grading.)

verdict: PASS
