review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`.

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `a86859da35221feef00405e0c095e0a2d20bb75210af188b81511d9626e0e50d`
- baseline: none (first review; no `--re-review`/`--baseline` given)
- reviewer model used: claude-sonnet-5-5
- Evidence checkable here: the spec, `.dev/orca-command-refactor/README.md`, and the three files under `inventory/`. Every citation outside those (`CLAUDE.md`, `src/...`, `pyproject.toml`, `Makefile`, `EVIDENCE.md`, the Orca guides) is UNVERIFIED unless the inventory line that quotes it supports it.
- Coverage: whole document, sections 1-9, Decisions and UNVERIFIED list. Experts applied: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (always active). Correctness focus is not active, so no State Variable Registry. Inventory line numbers for the 43-command table, depth limit, `worker_done`, heartbeat and subagent facts were checked against `inventory/*.md`.
- Brief clauses overridden: none.

## Result in one paragraph
The decision (Orca on top, commands as workers, no Orca calls inside commands) is consistent with the evidence it cites (`orca-capabilities.md:97-103,147-150,155-161`; `commands-a.md:35-55`, `commands-b.md:31-52`). The 10 / 27 / 6 split reconciles with the row counts in sections 3 and 4, and the phase table reconciles with the per-command phase column (35 phased commands = 27 + 8 ready commands with a fix). I found no stated text that causes a provably wrong build, a data-loss or a safety-boundary break. I found eleven Medium findings (places where an implementer must guess between two readings, or where a requirement is not stated) and a few minor notes. No finding is blocking.

## === REQUIREMENTS ANALYSIS ===

Grading: each finding passed the grading check (the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" needs no further assumption to be blocking). None did, so all are Medium or minor.

### F-01 Medium (MAJOR label) - Wiegers - citations that do not support the claim
- Spec:22 (E2) cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`". `orca-capabilities.md:161` is the pr-submit "top-level required" bullet, not a worker-start flag line (`orca-capabilities.md:161`).
- Spec:69 (WC-11) and spec:73 (section 2.3) cite `CAPS:115` for "`[G:placement]` lines 8-11: workers share the current worktree by default". `orca-capabilities.md:115` is "Worktrees are never deleted by these verbs"; `[G:placement]` appears only as a key at `orca-capabilities.md:17`, and no line I could read carries the "share the current worktree" claim. Treat that claim as UNVERIFIED.
- Spec:285 (UNVERIFIED item 14) says all 9 defects the citation check found "were fixed in place". Two defects of the same kind are still present, so that statement is overstated.
- Recommendation: correct both cites or mark them UNVERIFIED. Priority Low (WC-11's rule is sensible without the cite). Quality impact small.

### F-02 Medium (MAJOR label) - Wiegers/Adzic - `--unattended` is required in every brief, but two commands never gain it
- Spec:73 says the brief states "the exact command line including `--unattended`". Spec:84 (brainstorm) and spec:87 (init-lite) list "None" as the small fix, and the phase table gives them no phase (spec:158-162). Spec:76 says only changed commands gain the flag and the `## Unattended mode` section.
- Reading A: pass `--unattended` anyway (an undefined flag on those two commands; their behaviour is not stated). Reading B: omit it for those two. The text allows both, so this is Medium, not blocking.
- Recommendation: either list brainstorm and init-lite in P1 for the flag only, or state in 2.3 that the flag is passed only to commands whose section 3 row says they accept it. Priority Medium.

### F-03 Medium (MAJOR label) - Adzic - "refused under `--unattended`" has no defined outcome
- WC-2 defines three resolutions: default, caller flag, or blocked with a question (spec:60). Rows in section 3 say a flag is "refused" (business-panel socratic spec:102, cleanup/improve `--interactive` spec:103,110, explain interactive spec:108, pr-submit `--monitor 1` spec:114, roadmap `--interactive` spec:118, test `--watch` spec:123). "Refused" is none of the three, and "blocked" needs a question (spec:60), which a refusal does not have.
- Missing: the contract `status` for a refusal and the resulting `--outcome`. WC-5 maps `failed` and `blocked` to `failed` (spec:63), so the outcome is probably `failed`, but the text does not say it.
- Recommendation: add one sentence to WC-2: a refused flag writes `status: failed` with the refused flag named. Priority Medium.

### F-04 Medium - Wiegers - contract location is undefined for commands the brief gives no output directory
- WC-4 puts the contract at `<output-dir>/return-contract.yaml`, where `<output-dir>` is what the coordinator passed (spec:62).
- Section 3.1 briefs for cleanup-audit (`--pass <N>` only, fixed `.claude-audit/` output, spec:85), index-repo (no flag, spec:86), troubleshoot (no output flag, spec:91) and workflow (`--handoff none`, contract in `.dev/tasks/to-do/<id>/`, spec:92) pass no output directory. The location of the WC-4 contract for them is not stated; the P1 phase promises "the WC-4 contract" for them (spec:159) without a path.
- Contrast: spec:62 handles `--output <file>` commands (tdd, init-lite, spec-panel) by using the file's parent, so the rule is applied unevenly.
- Recommendation: add a "contract location" column to 3.1, or one rule for commands with a fixed output. Priority Medium.

### F-05 Medium - Cockburn - the primary actor of the blocked path is ambiguous (WC-2(c) vs WC-3 vs WC-5)
- WC-2(c) says a blocked gate writes `status: blocked` and stops (spec:60). WC-3 says the session "may instead" ask the coordinator once, wait, then re-invoke with the answer as a flag (spec:61). WC-5 maps `blocked` to `--outcome failed` (spec:63). AC-2.2 requires `worker_done --outcome failed` and no `agentWait` (spec:200).
- Not stated: whether the blocked contract is written before the `ask`, what happens to the contract file on a re-invocation (overwrite), and which path AC-2.2 tests when the worker chooses `ask` (it would end `succeeded` after a re-run, and `ask` is not an `agentWait`). The words "may instead" leave the choice to the worker, so a coordinator cannot predict the outcome of a gate.
- Recommendation: state which path the brief selects (for example "the brief says `ask-ok` or `block-only`"). Priority Medium.

### F-06 Medium - Wiegers - D4 touches Phase 2 rows, but Phases 1-3 are said to need no user decision
- Spec:154 and spec:225: "Phases 1-3 need no user decision". D4 (spec:244) lists auggie-review `--post-pr` and task `commit`/`push` as affected, both P2 rows (spec:100,121). WC-9 (spec:67) turns these off under `--unattended` and lets the brief turn them back on, which is exactly the D4 question.
- The default-off rule is safe on its own, so the phase can proceed, but the "no decision" claim is not strictly true: whether a brief may re-enable them is D4.
- Recommendation: say P2 implements the default-off half only, and the re-enable path waits for D4. Priority Low.

### F-07 Medium - Wiegers - SA-3 and WC-4 disagree on when the contract is written
- WC-4: written "in unattended mode" (spec:62). SA-3: written "only in unattended mode or when the caller passes the new output flag" (spec:148). A person who passes only the new output flag (for example a new `--output` on analyze) gets a contract under SA-3 and none under WC-4. AC-1.3 tests only the case with neither (spec:197).
- Recommendation: pick one trigger. Priority Low.

### Minor notes (never fail the review)
- N-1. Labels `M2`, `M3`, `M5` and "ladder rung 2" are used without a definition (spec:62, 159, 194, 195, 261). They look like ids from an earlier review round. A reader cannot resolve them.
- N-2. Decisions row for report shape says adversarial "already write[s] `return-contract.yaml`" (spec:261), while spec:83 says its filename is not fixed and `commands-a.md:97` says adversarial "promise[s] one without naming a path". Reword.
- N-3. WC-7 cites `INV-A:95` for "nesting loses tools at Claude Code's depth limit" (spec:65). `commands-a.md:95` says the opposite emphasis ("Top-level is not the blocker it looked like", nesting allowed up to three layers); the "loses Agent at the depth limit" text is at `commands-a.md:35`. Cite line 35, and keep the point that WC-7 is a precaution, not a proven blocker.
- N-4. WC-10's 4-minute wait limit rests on the heartbeat cadence taken from the worker's own preamble (`orca-capabilities.md:130`), and whether heartbeat age affects liveness is UNVERIFIED (`orca-capabilities.md:130,181` item 7). WC-10 is a cautious rule; label it so.

## === ARCHITECTURE ANALYSIS ===

### F-08 Medium - Fowler/Nygard - AC-C1 scans `src/superclaude/core`, yet Phase 0 adds Orca text there
- SA-5 and P0 add an Orca section to `HOW-WE-WORK.md` and a coordinator brief template to `core/WORKER-CONTRACT.md` (spec:150,158). SA-2 bans Orca calls only in "command, skill or agent" files (spec:147). AC-C1 scans commands, skills, agents **and core** for `orca[-ide] (orchestration|worktree|terminal|agent)` and requires no output (spec:172).
- A routing section that tells a reader how to dispatch ("orca-ide orchestration task-create ...", as spec:180 itself does) trips AC-C1. Whether P0 text avoids that phrasing is not stated. Reading A: the core files must avoid those exact words. Reading B: AC-C1 should exclude the two files. Medium, because the implementer must guess.
- Recommendation: either drop `core` from AC-C1 or exclude the two named files. Priority Medium.

### F-09 Medium - Fowler - AC-C5 ("edits are additive") conflicts with adding flags to Usage lines
- SA-4 allows "new flags" as additive (spec:149). AC-C5 fails on any removed line (`grep -E '^-[^-]'`, spec:176). Adding `--unattended` to an existing Usage line in a code block rewrites that line, which shows up as a removed line. Adding a second Usage line avoids it, as the spec-panel command already shows two Usage lines. Neither SA-4 nor AC-C5 says which.
- Recommendation: state that a new flag goes on a new Usage line, or let AC-C5 ignore Usage lines. Priority Medium.

### F-10 Medium - Newman/Hohpe - the integration contract has no version or schema owner
- The contract file is the only interface between commands and a coordinator (spec:62). It lists "at least" five fields, existing contracts keep their own fields (spec:62), and the check at spec:183 asserts only `status` and `command`. There is no `contract_version` field, although existing contracts already carry one (the workflow contract is "contract 1.1", `commands-b.md:272`). A later change to the shared field set cannot be detected by a coordinator.
- Recommendation: add `contract_version` to the required field list, or state why it is not needed. Priority Low-Medium.

### F-11 Medium - Nygard - timeouts and recovery of a worker that never writes the contract
- WC-4 says the file is written "on every outcome" (spec:62), and WC-5 says no report means `--outcome failed` (spec:63). A worker that dies, is stopped, or hits context limits writes nothing; the spec does not say how the coordinator detects this other than `worker-show` (spec:181), nor what happens to a half-written contract on `--retry-of` (WC-6 says resume or fresh directory; a stale `blocked` contract in a reused directory could be read as the new result). `orca-capabilities.md:80` shows a worker's own failed report does not trip the circuit breaker, but a missing report is not covered.
- Recommendation: one sentence: the coordinator treats a contract older than the dispatch as absent. Priority Low-Medium.

### Notes from the architecture pass
- Bounded context is clean: Orca facts live in the capabilities inventory, command facts in the two inventories, and the spec adds only the worker contract (spec:16, 147). The rejected alternative (spec:29-39) is supported by `orca-capabilities.md:97-103` (depth 1), `:147-150` (no Orca, no preamble), `:76,150` (`worker_done` pane binding).
- The evidence statement is honest about its main gap (no direct-route run; spec:43, `commands-b.md:323`). Phase 0 is the right place to close it, and AC-0.4 says a failure there reopens section 1 (spec:194).
- Outward actions are default-off (WC-9, spec:67), and the repo-fork rule is respected in the checks (spec:202, 209, 210 use `IronbellyOrg/IronClaude`).

## Whittaker adversarial pass (attacks on the spec's own rules)
- Sequence attack on WC-3/WC-5: worker asks, receives the answer, re-runs the command (contract overwritten), sends `worker_done succeeded`; the earlier `blocked` contract was never seen by the coordinator. The invariant "outcome matches contract status" holds, but the ask path is not tested. See F-05.
- Sentinel collision: `status: partial` maps to `succeeded` (spec:63, 263). A coordinator that reads only `--outcome` will not see partial work; the spec relies on the first sentence of the body. Acceptable (stated, spec:263), and no finding.
- Zero/empty attack on `<output-dir>`: empty or missing output flag in the brief. No rule says what the command does if the flag is absent under `--unattended` (refuse, or default path). WC-4 says the directory is "the directory the coordinator passed", so the absent case is unspecified. Medium, folded into F-04.
- Accumulation attack on WC-11: two workers write the same default output name; the spec fixes it with a timestamp or slug but cleanup-audit has a fixed directory (spec:85, noted there as one audit per worktree). Covered by the spec.

## Guard Condition Boundary Table
Guards found: the `--unattended` switch, the contract `status` mapping, the heartbeat/wait limit, the readiness limit, the confidence threshold (task, spec:121), and `<output-dir>` derivation. One row per input class that can occur; classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` present | WC-2, spec:60 | Zero/Empty | flag absent | false | standalone behaviour unchanged (SA-1, spec:146) | OK |
| `--unattended` present | WC-2, spec:60 | Typical | flag present | true | gate resolution per section 3 | OK |
| `--unattended` present | 2.3, spec:73 | Legitimate Edge Case | command with no phase (brainstorm, init-lite) | true | not specified | GAP (F-02) |
| refused flag | section 3 rows, spec:102-123 | Legitimate Edge Case | `--interactive`, `--watch` with `--unattended` | true | "refused"; contract status and outcome not stated | GAP (F-03) |
| contract `status` | WC-5, spec:63 | One/Minimal | `blocked` | `failed` | `--outcome failed` | OK |
| contract `status` | WC-5, spec:63 | Typical | `succeeded`, `partial` | `succeeded` | `--outcome succeeded` | OK |
| contract `status` | WC-5, spec:63 | Zero/Empty | no report / missing file | `failed` | `--outcome failed`; stale file from earlier run not addressed | GAP (F-11) |
| `<output-dir>` | WC-4, spec:62 | Zero/Empty | no output flag in the brief | n/a | not specified (3.1 rows cleanup-audit, index-repo, troubleshoot) | GAP (F-04) |
| `<output-dir>` | WC-4, spec:62 | Legitimate Edge Case | `--output` is a file | parent dir | parent dir, dedicated to the run | OK |
| wait size | WC-10, spec:68 | Maximum/Overflow | single call over 5 min | true | split into waits of at most 4 min | OK |
| wait size | WC-10, spec:68 | Legitimate Edge Case | cli-eval eval up to 3600 s | true | "split the eval wait" (spec:104); mechanism not stated | OK (mechanism covered by `commands-a.md:65`; approach is a design choice, not a gap) |
| readiness limit | WC-1, spec:59 | Maximum/Overflow | prompt fallback above ~45 s | true | start fails again (cited to `EVIDENCE.md:56`, which is UNVERIFIED here; quoted at `orca-capabilities.md:49`) | OK |
| confidence | task row, spec:121 | Typical | below 0.70 | true | blocked | OK |
| confidence | task row, spec:121 | Legitimate Edge Case | exactly 0.70 | false | not stated in the spec (threshold text lives in the task skill) | OK (inherited from `sk/sc-task-protocol`, UNVERIFIED) |
| heartbeat | WC-3, spec:61 | Typical | blocked inside `ask` | true | no heartbeat (`orca-capabilities.md:64`) | OK |

Classes left out: "One/Minimal" for `--unattended` (a flag has no size); "Sentinel Value Match" for the guards other than `status` (no sentinel values exist in them); "Maximum/Overflow" for `status` (closed four-value set, spec:62).

The table is complete (all cells populated, every guard enumerated), so FR-10 does not block synthesis. GAP rows are graded under FR-8: none names a concrete wrong outcome or a security/data-loss risk without a guess, so each GAP is Medium.

## Quantity Flow (pipeline dimensional analysis)
Triggered by the phase/command roll-up, which filters counts at each stage.

```text
[cmd/ commands: 43 (INV-A 21 + INV-B 22)] --> [Sec 3.1 ready: 10] + [Sec 3.2 needs change: 27] + [Sec 4 coordinator-only: 6] = 43   OK
[Sec 3.2: 27] + [Sec 3.1 with a fix (adversarial, cleanup-audit, index-repo, workflow, reflect, release-split, tdd, troubleshoot): 8] = 35 phased commands
[P1: 9 + 4 fixes = 13] + [P2: 15] + [P3: 4] + [P4: 3] = 35   OK
[brainstorm, init-lite: no phase, no change] --> [consumer: 2.3 brief "includes --unattended"] <-- MISMATCH (F-02)
```
No dimensional mismatch beyond F-02. The P1 row counts match the 3.2 phase column (analyze, build, business-panel, design, document, explain, index, load, test).

## UNVERIFIED citations (not checkable inside this sandbox)
`CLAUDE.md:16,50,72-83,157,334,408` (spec:52, 34, 150, 192, 239); `src/superclaude/cli/install_core.py:4,13-24,33` (spec:52); `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254` (spec:146, 164); `src/superclaude/core/CLAUDE.md:65` (spec:164); `pyproject.toml:38` (spec:183); `Makefile:68-74` (spec:279); all `cmd/` and `sk/` line cites not quoted by an inventory line; `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:35-56`, `.dev/codegraph-migration/orchestration/README.md:31,33,42` and `.../adversarial/return-contract.yaml:10` except where quoted at `orca-capabilities.md:49,156`; the E5 grep results dated 2026-11-02 (spec:25); the claim in spec:11 that 11 locations were re-read and in spec:285 that about 340 citations were checked. The Orca guide line cites (`[G]`, `[H:*]`) are verifiable only through the inventory lines that quote them, which I checked for lines 44-52, 58-80, 92-116, 128-130, 145-161 and 176-188.

## Follow-up candidates (Medium and minor; none blocking)
F-01 citation defects (CAPS:161, CAPS:115, spec:285 claim); F-02 `--unattended` for brainstorm/init-lite; F-03 outcome of refused flags; F-04 contract location for fixed-output commands; F-05 ask-versus-block path; F-06 D4 versus "no decision" in P1-P3; F-07 SA-3 versus WC-4 trigger; F-08 AC-C1 scope versus P0 core text; F-09 AC-C5 versus new Usage flags; F-10 contract version field; F-11 stale or missing contract on retry; N-1 undefined labels; N-2 adversarial contract wording; N-3 INV-A:95 cite; N-4 WC-10 rationale.
Issue question: this run is a labelled audit with no user in the loop, so the question "open an issue for these?" is recorded here for the coordinator to ask once; no issue was created.

## Reviser brief
None. There are no blocking finding ids. Per the Review Loop, Medium and minor findings never go in the Reviser brief and a brief cannot make them fail the review.

verdict: PASS
