review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the full document (no `--re-review`, no `--baseline`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `a6e5c8f0ff0545238ba19f3f7d98a7d4329bb51a628932a5ec8669cc448da770` (59005 bytes, 285 lines)
- baseline: none given (not a re-review)
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- brief clauses overridden: none
- citation key: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## What was covered

Read in full: the candidate, README, the three inventories, command.md, the review-loop prompt file. Checked: every `INV-A:N`, `INV-B:N`, `CAPS:N` and `README:N` citation in the candidate against the file it names (all resolve to the claimed content, with the exceptions listed under Medium findings); the 10 / 27 / 6 counts and the phase membership counts (9 + 11 + 4 + 3 = 27 for section 3.2, 15 for P2 and AC-2.2); the contract-path rule WC-4 against the per-command rows; the common and per-phase acceptance checks against the requirements they test.

NOT covered / UNVERIFIED (outside the sandbox, no file to check): every citation of the form `src/superclaude/...`, `sk/...`, `cmd/...`, `CLAUDE.md:N`, `Makefile:N`, `pyproject.toml:38`, `src/superclaude/core/HOW-WE-WORK.md:N`, `EVIDENCE.md:N`, `.dev/codegraph-migration/...`. Where one of these is repeated by an inventory, the inventory's wording was compared to the candidate's wording only. The candidate's own statements that it re-read 11 locations (SPEC:11) and that a validator re-read about 340 citations (SPEC:285) are UNVERIFIED. The E5 grep result (SPEC:25) is UNVERIFIED.

## Panel (fixed order, critique mode)

Active: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Requirements focus leads with Wiegers; architecture focus leads with Fowler.

## Mandatory artifact 1: Guard Condition Boundary Table

Guards in the candidate are the conditional rules with thresholds, enumerations or branch conditions. Classes left out are listed with a one-line reason. Built by Nygard, completeness checked by Crispin, attacked by Whittaker. Complete before synthesis (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--output` names a file vs a directory | WC-4 (SPEC:62) | Typical | `--output docs/x/TDD_A.md` | file branch | contract at parent dir `docs/x/return-contract.yaml` | GAP (see B-1: two workers, same parent dir, one path) |
| G1 | WC-4 | Legitimate Edge Case | `--output` absent (index-repo, cleanup-audit, research, save, recommend) | neither branch | not stated in WC-4; only the M3 fallback via `worker_done --report-path` (SPEC:62) | OK (fallback named) |
| G1 | WC-4 | Zero/Empty | `--output ""` | undefined | not stated | GAP (Medium F-6) |
| G2 workflow package id exists | WC-4 (SPEC:62) | Zero/Empty | no `<id>` yet (STOP before creation) | false | contract at `.dev/tasks/to-do/return-contract.yaml`, a fixed shared path | GAP (B-1) |
| G2 | WC-4 | Typical | `<id>` exists | true | `.dev/tasks/to-do/<id>/return-contract.yaml` | OK |
| G3 outcome mapping (report status) | WC-5 (SPEC:63) | Typical | `succeeded` | true | `--outcome succeeded` | OK |
| G3 | WC-5 | One/Minimal | `partial` | true | `--outcome succeeded`, body says partial; Decisions row at SPEC:263 gives the reason | OK |
| G3 | WC-5 | Sentinel Value Match | `blocked`, `failed`, or no report file | true | `--outcome failed` | OK |
| G3 | WC-5 | Legitimate Edge Case | status outside the four values (an existing contract's own vocabulary, SPEC:62 "keep their fields") | undefined | not stated; existing vocabularies not read | GAP (Medium F-4) |
| G3 | WC-5 | Legitimate Edge Case | `partial` | defined mapping, undefined meaning | no rule says when a command reports `partial` rather than `succeeded` or `failed` | GAP (Medium F-4) |
| G4 wait size | WC-10 (SPEC:68) | Typical | wait of 3 minutes | below 4 min | allowed | OK |
| G4 | WC-10 | Maximum/Overflow | single tool call over 5 minutes | true | must be split into waits of at most 4 minutes | OK |
| G4 | WC-10 | Legitimate Edge Case | wait of exactly 4 to 5 minutes | between split limit and heartbeat cadence | "longer than 5 minutes" triggers the split, "at most 4" is the result; 4 to 5 minute waits are neither required nor forbidden | OK (harmless: 4-minute rule is the target, Decisions row SPEC:266) |
| G5 `--unattended` present | WC-2 (SPEC:60) | Typical | flag present, gate hit | true | resolve by default, brief flag, or blocked | OK |
| G5 | WC-2 | Legitimate Edge Case | flag present together with a person-mode flag (`--interactive`, `--watch`, `--mode socratic`, `--format interactive`, `--monitor 1`) | true | "refused" in section 3 rows (SPEC:102, 103, 104, 108, 110, 114, 123); the refusal's outcome and report are not defined | GAP (Medium F-6) |
| G5 | WC-2 | Zero/Empty | flag present on a command in P1 whose gate conversion lands in P2 | true | P1 says the flag is "accepted" (SPEC:159), the gate is converted later (SPEC:160) | GAP (Medium F-3) |
| G5 | WC-2 | Sentinel Value Match | flag absent | false | standalone behaviour unchanged (SA-1, SPEC:146) | OK |
| G6 confidence `< 0.70` | task row (SPEC:121) | Typical / Max | 0.69 | true | blocked | OK |
| G6 | task row | Legitimate Edge Case | exactly 0.70 | false | not stated in the candidate (source threshold is "< 0.70", INV-B:199) | OK (inherited from source) |
| G7 nested-depth limit | R1, WC-8 (SPEC:33, 66) | Typical | depth 1 setting | true | worker may not start workers | OK |
| G7 | R1 | Legitimate Edge Case | user raises depth (D5 option b) | false | rejected alternative, D5 recommends keeping 1 | OK |
| G8 outward default | WC-9 (SPEC:67) | Typical | default pushes, opens a PR, posts to GitHub, installs, provisions | true | off | OK |
| G8 | WC-9 | Legitimate Edge Case | local folder move by default (reflect Wave 7, INV-B:114), live web search (research), real-model eval run (cli-eval) | undefined | "calls a paid external run" is not defined; the research and cli-eval rows do not say whether WC-9 turns them off | GAP (Medium F-5) |
| G9 parallel writes | WC-11 (SPEC:69) | Typical | two workers, timestamped default dirs | no collision | OK | OK |
| G9 | WC-11 | Legitimate Edge Case | two workers editing the same product file (cleanup, improve, implement, document inline) in one worktree | collision possible | only output paths and memory keys are covered; no rule on worktree placement for editing workers (SPEC:73 only says the brief states placement) | GAP (Medium F-7) |
| G10 heartbeat/ask | WC-3, WC-10 | Maximum/Overflow | `ask` timeout | true | resume same message ID, no duplicate | OK |

Classes omitted: Maximum/Overflow for G3, G5, G6, G8 and G9 (no numeric capacity in the text, and the only counts are the fixed 43 / 10 / 27 / 6); One/Minimal for G1, G2, G4, G5, G6, G7, G8 (boolean or enumerated guards with no one-item case); Sentinel for G1, G2, G4, G6, G7, G9 (no sentinel value in the rule).

Status summary: 5 GAP rows are Medium (F-3, F-4, F-5, F-6, F-7); 2 GAP rows for G1 and G2 feed blocking finding B-1.

## Mandatory artifact 2: Quantity Flow Diagram (pipeline dimensional analysis)

Triggered: the spec describes a 3-stage flow (inventory verdicts, then 5 phases, then per-phase acceptance checks) where counts split (FR-17). Fowler annotates, Whittaker attacks the divergence points.

```text
[Source: 43 commands (INV-A 21 + INV-B 22)] --> [Stage 1: verdict split]
    --> [10 ready (SPEC:78-92)] [27 needs change (SPEC:94-125)] [6 coordinator-only (SPEC:128-137)]    10+27+6 = 43  conserved
        |
        v
[Stage 2: phase assignment]
    P0: 0 edits, 3 smoke runs   (SPEC:158)
    P1: 9 (3.2 rows) + 4 fixes to ready commands   (SPEC:159)
    P2: 11 (3.2 rows) + 4 ready commands = 15      (SPEC:160)  AC-2.2: 9 blocked + 6 non-blocked = 15  conserved
    P3: 4    (SPEC:161)
    P4: 3    (SPEC:162)       9 + 11 + 4 + 3 = 27 conserved for 3.2
        |
        v
[Stage 3: contract delivery]
    commands whose rows name "contract" or "report path" in 3.2: 27 (all but load)
    ready commands that gain a contract in any phase: only adversarial, workflow named (SPEC:83, 92)
    ready commands with no named contract change: brainstorm (has one), cleanup-audit, index-repo, init-lite, reflect (has one), release-split, tdd, troubleshoot   <-- 6 without an assigned contract step (F-1)
    Consumer: AC-2.2 step 4 expects a contract with `status: blocked` for tdd, troubleshoot, release-split   <-- MISMATCH (F-1)
```

The 43 / 10 / 27 / 6 counts and the per-phase counts are conserved. The only divergence is Stage 3: WC-4 says every changed command writes the contract (SPEC:62) while the per-row assignment leaves six ready commands without a stated contract step (Medium F-1, because the text allows a reading in which P1's generic scope covers them).

## === REQUIREMENTS ANALYSIS ===

### Blocking

**B-1 — CRITICAL — Wiegers, Whittaker (Sequence/Divergence attack) — WC-4 puts the report file at a path two workers share, and WC-11 forbids that — priority High**

Location: WC-4 (SPEC:62) and WC-11 (SPEC:69).

Grading check: An implementer who follows the stated text as written builds a contract path of `<parent directory of --output file>/return-contract.yaml` for `tdd`, `init-lite` and `spec-panel`, and `.dev/tasks/to-do/return-contract.yaml` for a `workflow` run that stops before an `<id>` exists, and that is wrong because WC-11 says "Two workers in one worktree must never write the same file", and the second worker's write replaces the first worker's contract.

Concrete attack (state trace, Whittaker):
1. Coordinator dispatches worker W1 `/sc:tdd "auth service" --unattended --output docs/arch/TDD_AUTH.md` and worker W2 `/sc:tdd "billing" --unattended --output docs/arch/TDD_BILLING.md` in one worktree (the default placement, CAPS:115, SPEC:69). The tdd default location is `docs/[domain]/TDD_[COMPONENT-NAME].md` (INV-B:222), so same-domain TDDs share a parent by default.
2. WC-4 (SPEC:62): "when `--output` names a file (tdd, init-lite, spec-panel), `<output-dir>` is that file's parent directory". Both contracts go to `docs/arch/return-contract.yaml`.
3. W1 finishes `succeeded`; W2 stops `blocked` (bare topic, SPEC:90). Before: W1's file says `succeeded`. After W2 writes: the single file says `blocked`.
4. W1 sends `worker_done --outcome succeeded --report-path docs/arch/return-contract.yaml`. The coordinator opens that path (SPEC:62, 73), reads `blocked`, and by WC-5 and 7.2 step 3 sees an outcome that does not match the contract status. The same collision occurs with no setup at all for two `workflow` runs that both STOP before creating a package (SPEC:62: `.dev/tasks/to-do/` is a fixed path) and for two `init-lite` runs with default outputs (`.dev/superclaude/context-audit.md`, INV-A:55).
5. Side effect: a tracked `docs/` directory gains a `return-contract.yaml` next to the deliverable.

Why the acceptance checks do not catch it: AC-1.2 and AC-2.2 run one worker at a time (SPEC:196, 200); AC-3.4 is the only two-worker check and it covers `save` only (SPEC:207).

Recommendation (delete or narrow, no new mechanism): where `--output` names a file, name the contract `<output file stem>.return-contract.yaml` beside it, or require the coordinator to pass a per-worker directory; and give the pre-`<id>` workflow STOP a path that carries the slug or timestamp the coordinator passes (WC-11's own rule at SPEC:69).

Quality impact: removes the only path in the spec where a correct implementation reports the wrong worker's status.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The decision itself (Orca above, commands as units) is supported: E1 to E6 resolve against `CAPS:92,86,161,155` and `INV-A:76-83,94-98`, and the rejected alternative R1 to R5 resolves against `CAPS:97-103,145-150`. Fowler and Newman find the boundary clean: no command gains an Orca call (SA-2), and the contract file is the single shared interface.

## Follow-up candidates (Medium and minor; none triggers a revision)

Each Medium finding needs a guess about which reading an implementer picks, or is a requirement the document never states. Per the Review Loop rule 2 and the FIRST-REVIEW grading check they are not blocking.

### Medium

- **F-1 — Medium — Wiegers, Adzic — Contract step is not assigned for six ready commands — priority Medium.** WC-4 requires `return-contract.yaml` on every outcome (SPEC:62). Section 3.1 says the worker "reports the named file until Phase 1 adds the contract" (SPEC:79), but the P1 command list names only adversarial, cleanup-audit, index-repo, workflow among the ready commands (SPEC:159), the 3.1 rows for tdd, troubleshoot and release-split change only the gate (SPEC:89-91), AC-1.1 excludes 3.1 rows whose small fix is `None` from the `## Unattended mode` section test (SPEC:195), and AC-2.2 expects `status: blocked` plus `blocked_question` from tdd, troubleshoot and release-split (SPEC:200). Troubleshoot writes a contract only with `--caller task-unified` (INV-B:242). A reader who takes the P1 scope sentence ("The WC-4 contract in unattended mode", SPEC:159) as covering them is fine; one who follows the Commands column is not. State which. Rationale: unlisted contract steps make AC-2.2 unpassable for the second reader.
- **F-2 — Medium — Nygard — `--unattended` is required in every brief but does not exist before P1 — priority Medium.** Section 2.3 says the brief carries "the exact command line including `--unattended`" (SPEC:73); the flag is added in P1 (SPEC:159); the P0 smoke runs omit it (SPEC:194). A coordinator that follows 2.3 in P0 passes a flag the command does not define. Narrow 2.3 with "from P1 on".
- **F-3 — Medium — Nygard — P1 accepts the flag on gated commands before their gates are converted — priority Medium.** P1 adds `--unattended` to every 3.1 and 3.2 command and calls it a no-op "where a command has no gate" (SPEC:159); gated commands are converted in P2 to P4 (SPEC:160-162). Between phases `/sc:cleanup --unattended` is accepted and still prompts, which is the silent stall WC-2 exists to prevent (SPEC:60, INV-A:62). Either scope P1's flag to the no-gate commands or say gated commands refuse the flag until their phase.
- **F-4 — Medium — Wiegers — Contract status vocabulary is fixed without reading the existing vocabularies, and `partial` is undefined — priority Medium.** WC-4 requires `status` in four values and also says commands with a contract "keep their fields" (SPEC:62); 7.2 step 4 asserts the four-value set (SPEC:183). No cited line shows the existing `status` values of workflow, brainstorm, reflect, adversarial (INV-B:272 names the field only), so a conflict is possible and is UNVERIFIED. No rule says when a command reports `partial` (SPEC:63, 263 only map it).
- **F-5 — Medium — Nygard, Hightower — "paid external run" is undefined in WC-9 — priority Medium.** WC-9 turns off any default that "calls a paid external run" under `--unattended` (SPEC:67). Research's whole function is Tavily and Playwright web search (INV-B:134) and cli-eval run executes real eval runs (INV-A:44); their rows say nothing about WC-9 (SPEC:104, 116). Local folder moves by reflect Wave 7 (INV-B:114) are also not classified. Define the term or list the commands it turns off.
- **F-6 — Medium — Whittaker (Zero/Empty attack) — "refused" is not an outcome — priority Medium.** Section 3 rows refuse `--interactive`, `--watch`, `--mode socratic`, `--format interactive`, `--monitor 1` under `--unattended` (SPEC:102-104, 108, 110, 114, 123), while WC-4 demands a contract "including stops before any other output exists" (SPEC:62). Which status a refusal reports is not stated; also `--output ""` is unspecified (guard table G1).
- **F-7 — Medium — Cockburn, Newman — No rule for parallel editing workers in one worktree — priority Medium.** WC-11 covers default output paths and memory keys only (SPEC:69). Cleanup, improve, implement and inline `document` edit product files (INV-A:43, 47, 51, 52), and the default placement is the shared worktree (SPEC:69, CAPS:115). Section 2.3 only says the brief states the placement (SPEC:73). This is a requirement the document never states.
- **F-8 — Medium — Fowler — Tasklist row drops an unverified premise and a top-level requirement — priority Medium.** The inventory says Stage 10.5's reflect fan-out "must run at the worker's top level" and marks nested spawning UNVERIFIED (INV-B:215, 210, 322). The spec's row says the fan-out "runs one layer below the worker, inside Claude Code's nesting limit" and requires no change (SPEC:122), citing INV-A:14. Reflect Tier 2 itself spawns reviewers and adversarial agents below that layer (INV-B:111), so "one layer" describes the reflect agents, not their children. Restore the UNVERIFIED marker or the inventory's requirement.
- **F-9 — Medium — Hohpe, Wiegers — SA-2, 2.1 and P0 describe the contract file's Orca content differently — priority Medium.** Section 2.1 says unattended mode "names no Orca command" (SPEC:51). P0 puts all of section 2, including WC-5 `worker_done` and WC-12 `check`, into `WORKER-CONTRACT.md` in `src/superclaude/core` (SPEC:52, 158). SA-2 allows an Orca mention only "as an example of a caller's question channel inside the contract file" (SPEC:147). AC-C1 greps `src/superclaude/core` with no exemption for that file or for the new Orca section in `HOW-WE-WORK.md` (SPEC:172, 158). Which rules live in the contract file, and whether AC-C1 exempts it, is not stated.
- **F-10 — Medium — Crispin — AC-C5 and the usage line — priority Medium.** AC-C5 passes only if no existing line is deleted (SPEC:176) while SA-4 permits "new flags" (SPEC:149). Adding a flag to an existing Usage line deletes that line in the diff. Only `load`'s usage line is named as an exempt defect fix.
- **F-11 — Medium — Cockburn — The README's readiness evidence is narrowed without evidence — priority Medium.** README says a worker that waits on a question fails Orca's 60-second limit (README:14, INV-A:17). Section 1.4(2) says a command's own question "comes after readiness" (SPEC:44), but `CAPS:47` records that for Claude the task is passed on the command line, so the command starts before Orca sees a fresh input box. The conclusion (WC-2 forbids the prompt) is unaffected; the claim should carry UNVERIFIED.
- **F-12 — Medium — Adzic — WC-3 and AC-2.2 disagree on how a blocked gate ends — priority Medium.** WC-3 lets the worker `ask` the coordinator instead of ending (SPEC:61); AC-2.2 requires `worker_done --outcome failed` on the same input (SPEC:200). The test result depends on which path the worker takes.

### Minor notes

- N-1: Markers `(M1)` to `(M5)` appear in SPEC:62, 73, 182, 194-196, 200 and are defined nowhere in the document.
- N-2: UNVERIFIED list item 14 (SPEC:285) records a completed check, not an unverified item, so the list mixes two kinds of entry.
- N-3: AC-C1 to AC-C5 show `\|` inside backticks in a table (SPEC:172, 175, 176); a raw copy into `grep -E` reads `\|` as a literal pipe and the check then passes vacuously. Rendered GFM removes the backslash.
- N-4: AC-2.4 counts reviews and comments with `--jq length` without `--paginate` (SPEC:202); a PR with 30 or more entries would show "unchanged".
- N-5: AC-1.3's example choice is safe, but "two P1 commands" (SPEC:197) includes workflow and adversarial, which write a contract in plain runs today (INV-B:272, INV-A:35); the check must pick commands that do not.
- N-6: E3 cites `invocation_method: "skill-direct"` as support (SPEC:23) while section 1.4(1) says the same run proves only the nested route (SPEC:43). The tension is disclosed but not reconciled.
- N-7: `AC-1.2` passes `--output <dir>` to index-repo and cleanup-audit (SPEC:196), which take no such flag (SPEC:85, 86).

## Whittaker adversarial section (consolidated)

| # | Attack | Invariant location | Triggering condition | Outcome | Severity |
|---|---|---|---|---|---|
| W-1 | Sequence attack (two writers, one path) | WC-4 vs WC-11 (SPEC:62, 69) | two workers whose contract path resolves to one directory | second write replaces first; coordinator reads the wrong status | CRITICAL (B-1) |
| W-2 | Divergence attack (flag accepted vs honoured) | P1 scope (SPEC:159) | `--unattended` on a gated command before its phase | silent stall | MAJOR graded Medium (F-3) |
| W-3 | Sentinel collision (`partial`) | WC-5 (SPEC:63) | `partial` run that left no usable deliverable | mapped to `succeeded` | MAJOR graded Medium (F-4) |
| W-4 | Zero/Empty attack (refusal outcome) | WC-2, section 3 rows | person-mode flag together with `--unattended` | no defined status or contract | MAJOR graded Medium (F-6) |
| W-5 | Accumulation attack | WC-11 | N editing workers in one worktree | file collisions | MAJOR graded Medium (F-7) |

## Panel consensus and disagreements

- Consensus: the decision (Orca coordinates, commands stay units) is well supported; counts and phase membership are internally consistent; the contract file design is the right single interface.
- Consensus: the only defect that changes what an implementer builds without a guess is B-1.
- Disagreement: Wiegers would grade F-1 and F-4 blocking because AC-2.2 and 7.2 step 4 cannot pass on one reading; Nygard and Crispin hold they are Medium because the P1 scope sentence supports the passing reading and an implementer is not forced to pick the worse one. Graded Medium under the FIRST-REVIEW rule.

## Quality metrics (0 to 10)

Clarity 7.5, Completeness 7.5, Testability 7.0, Consistency 7.0.

## Follow-up issue question

Medium and minor findings above are the `follow-up candidates`. This run could not ask the user whether to open an issue for them and created none; the coordinator should put the question to the user once for this loop.

## Reviser brief

Blocking finding ids: **B-1**.

The reviser reads this report, not the command. Rules:
- Revise only text a blocking finding names (here WC-4 at SPEC:62 and, if needed, the matching sentence of WC-11 at SPEC:69).
- Add no rule, mechanism or section that B-1 does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone; do not award a PASS.

verdict: FAIL
