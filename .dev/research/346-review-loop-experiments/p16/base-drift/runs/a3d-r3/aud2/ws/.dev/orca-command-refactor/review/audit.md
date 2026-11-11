review: 1 of 3

# /sc:spec-panel audit: Orca worker contract spec (whole-document, first review)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (called `S` below; `S:N` = line N)
- candidate sha256: `ee66feb509d270d43ad6b910ad610ca80e6ec53ce17ddf42d33226ff403c6470`
- baseline: not given (first review, nothing to compare; `--re-review` and `--baseline` not used)
- reviewer model actually used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; format: standard markdown
- shared context read first: `.dev/orca-command-refactor/README.md` (1-38). Evidence I could check: `inventory/commands-a.md` (`INV-A`), `inventory/commands-b.md` (`INV-B`), `inventory/orca-capabilities.md` (`CAPS`). Review procedure: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- brief clauses overridden: none. Note: README:26 names `review/spec-panel.md` for the Task 5 review; this brief assigns `review/audit.md` and labels the run a whole-document audit, so I followed the brief.

## Coverage

Covered: all 285 lines of S (sections 1-9, Decisions, UNVERIFIED list). Checked against the inventories: the 43/10/27/6 split (S:76), every `INV-A:N` and `INV-B:N` row/line citation I could resolve (rows INV-A:35-55, INV-B:31-52, INV-A:76-98, INV-B:285-299, 301, 311, 320, 323), and the `CAPS:N` citations behind the worker contract, nesting depth, outcome, report-path and placement claims.

Not checkable in this sandbox, so UNVERIFIED: every citation into `src/superclaude/...` (the `cmd/` and `sk/` lines in sections 3, 4, 6), `CLAUDE.md:N` (S:34, 52, 147, 150, 164, 175, 192, 239, 264), `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:N`, `.dev/codegraph-migration/...`, `pyproject.toml:38`, `Makefile:68-74`, and the 11 "re-read" locations at S:11. I did not run any command from section 7.

Counts that do reconcile: 21 + 22 = 43 (`INV-A:3`, `INV-B:3`); 3.1 has 10 rows (S:83-92), 3.2 has 27 rows (S:99-125), section 4 has 6 rows (S:132-137); P1-P4 command lists add to 27 for the section 3.2 commands (9 + 11 + 4 + 3); P2 lists 11 from 3.2 plus reflect, release-split, tdd, troubleshoot from 3.1.

## Panel (fixed order, 11 experts; Whittaker at position 6)

Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower each reviewed. Hohpe, Newman, Gregory and Hightower raised nothing blocking beyond what is listed; their notes are folded into the findings by id.

## Grading check for each blocking finding

### B-1 (Wiegers, Crispin, Fowler): AC-1.1 cannot pass against the spec's own Phase 1 scope
Sentence: An implementer who follows the stated text as written builds a Phase 1 that touches 13 commands (S:159 lists analyze, build, business-panel, design, document, explain, index, test, load, plus fixes to adversarial, cleanup-audit, index-repo, workflow), and that is wrong because AC-1.1 (S:195) asserts that every one of the 37 commands in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`, so the phase's own pass condition fails for 24 commands, and S:154 ("Later phases do not start until the earlier phase's checks pass") then blocks P2-P4.

Evidence, all in S:
- S:159: P1 scope is "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" but its command list names 13.
- S:79: ready commands get "only ... the small fixes in the last column"; brainstorm (S:84) and init-lite (S:87) say "None", and neither is in the P1 list (S:159).
- S:112 and S:265: `load` writes no report and "a report file would be an unrequested addition", yet AC-1.1 requires its section to name `return-contract.yaml`.
- S:139 and S:240-242: `pr-submit` is a worker candidate only if D3 is accepted; the recommended D3(a) says "no pr-submit changes in Phase 4". S:114 and S:162 assign pr-submit's contract and gate resolutions to P4. AC-1.1 forces a pr-submit section naming `return-contract.yaml` in P1, before D3 is answered. S:154 and S:225 say P1-P3 need no user decision and proceed on the recommendations.
- P2 and P4 gate resolutions are defined per command (S:100-125) and scheduled later (S:160, S:162), so a P1 section for those commands cannot yet carry them.
- Count trace: expected sections 37 (S:195) versus commands in P1 scope 13 (S:159) versus ready-no-change rows 2 (brainstorm, init-lite).

### B-2 (Adzic, Crispin, Nygard): AC-0.4 is unpassable as written, and its dispatched command lines contradict the brief rule
Sentence: An implementer who follows the stated text as written runs the P0 smoke runs with commands that no command yet accepts `--unattended` for, and judges step 3 of 7.2 against a WC-4 contract path and a contract `status` that do not exist until P1, and that is wrong because AC-0.4 (S:194) says "steps 1-3 and 5-7 pass", while S:182 (step 3) requires the `worker_done` report path to be the WC-4 contract path and the outcome to match the contract's `status`, and S:194 itself says "the contract arrives in P1". The gate P0 must pass before P1 (S:154) therefore cannot be passed, and a failure "reopens section 1" (S:194).

Evidence in S: S:73 (brief carries the exact command line including `--unattended`), S:159 (the flag is added in P1), S:194 (smoke command lines have no `--unattended`), S:180-182, S:62 (WC-4 contract is written only in unattended mode).

## === REQUIREMENTS ANALYSIS ===

Findings are listed highest first. Blocking: B-1, B-2 (above). Everything below is Medium (a warning under `follow-up candidates`, no revision triggered) or a note.

| id | severity as labelled | expert | graded | finding | priority | quality impact |
|---|---|---|---|---|---|---|
| M-1 | MAJOR | Wiegers | Medium | WC-4's heading says the report is "known before dispatch" (S:62) but the ready workflow command writes `.dev/tasks/to-do/<id>/return-contract.yaml` with an id generated at run time (S:92; `INV-B:272`), and research, index-repo and cleanup-audit name paths the brief does not fix (S:85-86, S:116). Step 3 of 7.2 requires the report path to equal the WC-4 path (S:182). No text says what the contract path is when `--unattended` is passed with no `--output`/`--output-dir` (WC-4 assumes the coordinator passed one). Needs a guess to be wrong, so Medium. | Medium | clarity -1 |
| M-2 | MAJOR | Wiegers | Medium | WC-4 says commands that already write a contract "keep their fields" (S:62) and also requires `status` to be one of four values (S:62, S:262). The existing statuses of workflow, reflect, brainstorm and adversarial contracts are not recorded in the inventories I can read (`INV-B:272`, `INV-B:112`, `INV-A:97` name the files, not the values). Possible clash is unverified. | Medium | testability -1 |
| M-3 | MAJOR | Cockburn | Medium | `--unattended` ships on gated commands (cleanup, task, cli-eval, auggie-review, implement, post-release, pr-submit) in P1 (S:159) while their gate resolutions arrive in P2-P4 (S:160-162). In that window the flag exists but WC-2 (S:60) is false for those commands, and nothing in section 2.3 or section 6 tells a coordinator not to dispatch them yet. A worker would stall silently (S:44, S:60). Reads as a guess that someone dispatches early, so Medium. | High | completeness -1 |
| M-4 | MAJOR | Wiegers | Medium | S:154 and S:225 say P1-P3 need no user decision, but D4 (S:244) names auggie-review `--post-pr` and task `commit`/`push`, both P2 rows (S:100, S:121), and S:100 states the D4(a) outcome unconditionally. D4(b) ("Never") would remove the `--post-pr` return. Recommendation (a) makes this harmless. | Low | consistency -0.5 |
| M-5 | MAJOR | Adzic | Medium | WC-11 (S:69) and AC-3.4 (S:207) rely on per-session keys `<key>-<session-or-timestamp>.md` (S:119). The timestamp resolution and the preference between session id and timestamp are not stated, so two workers started in the same second can pick the same name. | Medium | testability -0.5 |
| M-6 | MAJOR | Crispin | Medium | WC-10 (S:68) splits Bash/poll waits to 4 minutes but a single Agent-tool fan-out call (adversarial with up to 10 agents, tdd research, troubleshoot Tier 2) also blocks the session longer than the 5-minute heartbeat cadence, and no requirement covers it. The spec itself notes absent heartbeats do not authorize stop (`CAPS:37`), so the harm is a coordinator misreading liveness; Medium. | Low | completeness -0.5 |

## === ARCHITECTURE ANALYSIS ===

| id | severity as labelled | expert | graded | finding | priority | quality impact |
|---|---|---|---|---|---|---|
| M-7 | MAJOR | Fowler | Medium | AC-C1 (S:172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and must print nothing, but P0 adds an Orca section to `HOW-WE-WORK.md` (S:158, S:150) and WC-3 / SA-2 (S:61, S:147) allow the contract file to mention Orca's `ask` as a question channel. If either text names the verb (`orca orchestration ask`), AC-C1 fails in P0. The spec does not say how the Orca section avoids the pattern. | Medium | consistency -1 |
| M-8 | MAJOR | Nygard | Medium | Tasklist Stage 10.5 depends on reflect's `--unattended` headless rule (S:122) and both are P2 (S:160) with no ordering inside the phase. Whether reflect's existing headless rule auto-accepts remediation hand-offs (the rule at `sk/sc-reflect-protocol/refs/remediation-handoff.md:239-247`, UNVERIFIED) decides what tasklist produces unattended; UNVERIFIED item 9 (S:280) adds that reflect may not treat an Orca worker as headless. `INV-B:295` recommended removing the nested remediation; S:122 chose to pass the flag instead without recording why in Decisions (S:258-269). | Medium | architecture -0.5 |
| M-9 | MAJOR | Newman | Medium | WC-10 for pr-submit: the wait is "a sleep of at least `--poll-interval`" (S:68). A caller-supplied interval of 240 s or more makes every iteration exceed the 4-minute split, and no clamp is stated. Only matters under D3(b). | Low | testability -0.5 |
| M-10 | MAJOR | Hohpe | Medium | 7.2 step 1 uses `worker-start --worktree current` (S:180). `CAPS` records only `--worktree <explicit_placement>` (`CAPS:116`) and the placement text "current or an exact existing workspace" (`CAPS:115`); `current` as a literal value is UNVERIFIED. Step 5 greps the transcript for `AskUserQuestion` (S:184), and a transcript that includes a loaded skill file will contain the word; the pass text says "call", but the check as scripted is a string search. AC-0.4 runs three workers in one worktree (S:194), so step 6's `git status --short` (S:185) would show the other workers' files unless they run one at a time, which is not stated. | Low | testability -0.5 |
| M-11 | MINOR | Gregory | Medium | Decisions and section 6 say P0 "tests the decision before anything is built on it" (S:158), but P0 first writes the contract file, the `KNOWN_CORE_FILES` entry, the HOW-WE-WORK section and the test file, then runs the smoke runs. The ordering is the reverse of the claim; harmless because P0 touches no command. | Low | clarity -0.25 |

## === ADVERSARIAL ANALYSIS (Whittaker) ===

I can break this specification by **Sequence Attack**. The invariant at **S:154 + S:195 (a phase passes only when all its checks pass)** fails when **AC-1.1 asserts 37 sections while P1 scope is 13**. Concrete attack: before: master has 0 `## Unattended mode` sections; implement P1 exactly as S:159 lists, so 13 commands gain one (state: 13 sections); run `uv run pytest tests/skills/test_worker_contract.py` per AC-1.1 (S:195); after: 24 commands fail the assertion (state: P1 cannot pass), so P2 (S:154) never starts. Finding: B-1.

I can break this specification by **Sequence Attack**. The invariant at **S:154 + S:194 (P0 must pass before P1)** fails when **step 3 of 7.2 is judged against a contract that P1 creates**. Concrete attack: before: no command writes a WC-4 contract; run `/sc:troubleshoot "<symptom>"` as a worker (no `--unattended`, S:194); the worker reports its `REPORT.md` (S:91); after: step 3 expects the report path to be the WC-4 path and the outcome to match a contract `status` (S:182) and finds neither, so P0 cannot pass. Finding: B-2.

I can break this specification by **Divergence Attack**. The invariant at **S:62 (WC-4, path known before dispatch)** fails when **the command allocates its own output id**. Concrete attack: coordinator dispatches `/sc:workflow "<change>" --handoff none` (S:92) and records the expected path `<output-dir>/return-contract.yaml`; workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml` for a fresh `<id>`; the coordinator opens a file that does not exist and sees no report. Finding: M-1.

I can break this specification by **Zero/Empty Attack**. The invariant at **S:62 (contract written on every outcome)** fails when **`--unattended` is passed with no `--output` or `--output-dir`**. Concrete attack: `/sc:analyze src/x --unattended` (analyze row S:99 says "add `--output`"); no directory exists, so the contract path is undefined and "stops before any other output exists" (S:62) has no place to write. Finding: M-1 (Medium, requirement never stated).

I can break this specification by **Accumulation Attack**. The invariant at **S:69 (WC-11, parallel-safe writes)** fails when **two `/sc:save --unattended` workers start in the same timestamp unit**. Concrete attack: two workers in one worktree both write `last_session-<ts>.md` with equal `<ts>`; the second overwrites the first; AC-3.4 (S:207) expects two files and sees one. Finding: M-5.

I can break this specification by **Sentinel Collision Attack**. The invariant at **S:62 (file-valued `--output` gives sibling `<stem>.return-contract.yaml`)** fails when **two deliverables share a stem**. Concrete attack: `--output docs/a.md` and a second run `--output docs/a.json` in the same directory both map to `docs/a.return-contract.yaml`. Note only (MINOR): the spec does not say how a command decides that `--output` names a file rather than a directory.

## Guard Condition Boundary Table

Guards identified: G1 readiness limit (S:59), G2 the `--unattended` switch (S:51, S:60), G3 outcome mapping (S:63), G4 wait/heartbeat split (S:68), G5 `--output` file versus directory (S:62), G6 confidence below 0.70 (S:121), G7 nesting depth 1 (S:33, S:66). Classes left out: Maximum/Overflow for G2, G3, G6 (no numeric capacity); Sentinel Value Match for G1, G4, G6, G7 (no sentinel in the text); One/Minimal for G2, G3 (boolean/enumerated).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 readiness limit | S:59 | Zero/Empty | `--timeout-ms 0` | falls to 60 s default | `CAPS:44` says non-positive uses the default; S:59 cites `CAPS:44-45` | OK |
| G1 | S:59 | Typical | 30 s fallback | pass | S:59 (passes with 30 s fallback, EVIDENCE.md:45,56 UNVERIFIED here) | OK |
| G1 | S:59 | Maximum/Overflow | fallback above about 45 s | fails | S:59 says it fails again; no maximum fallback is required numerically ("well inside") | OK |
| G1 | S:59 | Legitimate Edge Case | caller raises `--timeout-ms` (`CAPS:45`) | longer wait | S:59 mentions the per-start flag only as evidence | OK |
| G2 `--unattended` | S:51, S:60 | Zero/Empty | flag absent | false | SA-1 (S:146): today's behaviour | OK |
| G2 | S:60 | Typical | flag present, all gate flags supplied | true | WC-2 (a)/(b) | OK |
| G2 | S:60 | Legitimate Edge Case | flag present, no output dir given | true | none stated (M-1) | GAP |
| G2 | S:159 | Legitimate Edge Case | flag present on a gated command before its phase | true | none stated (M-3) | GAP |
| G3 outcome mapping | S:63 | Zero/Empty | no report exists | failed | `--outcome failed` | OK |
| G3 | S:63 | Typical | status `succeeded` | succeeded | stated | OK |
| G3 | S:63, S:263 | Legitimate Edge Case | `partial` or audit verdict FAIL | succeeded | stated; first body sentence carries the status | OK |
| G3 | S:63 | Legitimate Edge Case | `blocked` | failed | stated; interaction with WC-3 `ask` is "may" (S:61) | OK |
| G4 wait split | S:68 | Zero/Empty | wait of 0 s | no split needed | not stated | OK (cannot matter) |
| G4 | S:68 | Typical | one wait under 4 min | pass | stated | OK |
| G4 | S:68 | Maximum/Overflow | single Agent-tool call over 5 min | no heartbeat | none stated (M-6) | GAP |
| G4 | S:68 | Maximum/Overflow | `--poll-interval` of 240 s or more | exceeds 4 min | none stated (M-9) | GAP |
| G5 `--output` kind | S:62 | Typical | directory | `<dir>/return-contract.yaml` | stated | OK |
| G5 | S:62 | Typical | file | `<stem>.return-contract.yaml` beside it | stated, with an example | OK |
| G5 | S:62 | Sentinel Value Match | two files with one stem | same sibling name | none stated | GAP |
| G5 | S:62 | Legitimate Edge Case | path with no extension, or an existing directory named like a file | ambiguous | none stated | GAP |
| G6 task confidence | S:121 | Typical | below 0.70 | blocked | stated | OK |
| G6 | S:121 | Legitimate Edge Case | exactly 0.70 and the 0.70-0.89 band | not specified | S:121 says only "below 0.70"; `INV-B:199` quotes "<70%" so 0.70 is not blocked | OK |
| G7 depth 1 | S:33, S:66 | Typical | command calls `worker-start` | refused | stated, enforcement call sites UNVERIFIED (`CAPS:103`) | OK |

GAP rows and grading (FR-8, FR-9): the G2/G5 output-directory GAP and the G2 pre-phase GAP carry no concrete wrong outcome an implementer would produce from stated text, so both are Medium (M-1, M-3). The G4 rows are Medium (M-6, M-9). The G5 sentinel/edge rows are minor notes. The table is complete (FR-10).

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Triggered: the spec describes a staged classification and rollout where counts change (S:76, S:156-162, S:195).

```text
[Commands in src: 43 (21 INV-A:3 + 22 INV-B:3)] --> [Classify]
    --> ready 10 (S:83-92)          --> P0 smoke 3 of 10 (S:158); P1 fixes 4 of 10 (S:159); P2 fixes 4 of 10 (S:160)
    --> needs change 27 (S:99-125)  --> P1 9, P2 11, P3 4, P4 3 = 27 (S:159-162)  [conserved]
    --> coordinator-only 6 (S:132-137) --> no phase [conserved: 10 + 27 + 6 = 43]
[P1 scope text S:159: flag on 37 commands (3.1 + 3.2)] --> [P1 command list S:159: 13 commands]
    --> [AC-1.1 S:195: 37 sections expected, 13 produced]  <-- MISMATCH (B-1)
[Brainstorm and init-lite: 3.1 "None" S:84,87] --> [AC-1.1 expects a section on each] <-- MISMATCH (B-1)
[pr-submit: P4, and coordinator-only under D3(a) S:114,S:240] --> [AC-1.1 expects a P1 section] <-- MISMATCH (B-1)
```

The 43/10/27/6 and P1-P4 counts are conserved. The only divergence is the P1 scope-versus-AC-1.1 count.

## Follow-up candidates (Medium and minor; none triggers a revision)

- M-1 contract path when no output is given and for run-allocated ids (workflow, research, index-repo)
- M-2 `status` vocabulary versus existing contracts
- M-3 `--unattended` accepted on gated commands before their phase
- M-4 D4 touches P2 rows
- M-5 per-session key name collision
- M-6 heartbeat gap during long Agent-tool calls
- M-7 AC-C1 pattern versus the Orca section and the contract file
- M-8 tasklist depends on reflect inside P2; why the inventory's removal advice was not taken
- M-9 `--poll-interval` has no upper clamp
- M-10 `--worktree current` literal, the transcript string search, concurrent smoke runs
- M-11 P0 ordering versus the "tests the decision first" claim
- Notes: (N-1) `INV-A:95` is cited for "never inside a subagent" (S:65) but that line says top-level "is not the blocker it looked like" and names the depth-limit risk; the citation supports only the depth-limit half. (N-2) File-versus-directory detection of `--output` (G5). (N-3) All `src/`, `CLAUDE.md`, EVIDENCE.md and PR #329 citations are UNVERIFIED in this sandbox.

The loop asks the user once per loop whether to open an issue for these; this worker has no channel to the user in the sandbox, so the list is recorded only and no issue was created.

## Expert consensus

Agreed: the decision (Orca coordinates, commands stay units of work, S:13-45) is well supported by `CAPS:97-103,148-150` and `INV-A:76-98`, `INV-B:289-299`; the 43/10/27/6 classification matches the inventories; the three-gap statement of evidence strength (S:41-45) is honest. Disagreement: none between experts. The blocking defects are acceptance-check and phase-scope inconsistencies, not design errors.

Panel recommends `--focus correctness` for the next pass only if the spec adds counters or timers beyond the 4-minute and 5-minute rules; advisory only.

## Reviser brief

Blocking finding ids: B-1, B-2.

Reviser rules (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings (M-1 to M-11, notes) alone.
- Return the candidate once and do not award a PASS.

verdict: FAIL
