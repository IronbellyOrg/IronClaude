review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (spec-panel, critique mode)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec; a first review of the whole document (no `--re-review`, no `--baseline`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines
- candidate sha256: `032a73216d9fa2a2e58b2be6fa0c2ed6374df75cb60076a9b7d7f4bd03d07a67`
- baseline sha256: not applicable (first review)
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full. Grading uses the "implementer builds X, and X is wrong because Y" test (`...prompts.md:31`) and `command.md:259`.
- evidence readable in the sandbox: `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`. Citations below use `SPEC:N` for the candidate, `INV-A:N`, `INV-B:N`, `CAPS:N` for the inventories (same convention as `SPEC:8`), and `README:N`.
- not checkable here, so UNVERIFIED: every citation into `src/`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `/opt/Orca/...` and the `orca-ide` guides. I checked only that the spec's `INV-*`, `CAPS:*` and `README:*` line references land on the text claimed.

## Coverage

- Read in full: the spec, `README.md`, `orca-capabilities.md`, `commands-a.md`, and `commands-b.md` lines 1-60 and 265-323 (summary tables and verdict rows; the per-command notes between were not read in full).
- Spot-checked about 45 `INV-*`/`CAPS:*`/`README:*` references. All landed on the claimed text. Checked: `CAPS:44-45,46,52,58-61,64,66-67,68,72-74,76-79,86,92,97-103,107-113,115,116,128-130,135-139,145-151,155-161,178,180,186-188`; `INV-A:3,14,35-55,60-66,76-83,90-98,106,113,118,120`; `INV-B:3,31-52,285-286,289-301,311,320,323`; `README:6,11-17,30,31,35`.
- The 43 = 10 + 27 + 6 split matches both inventory summaries (`INV-A:73` 5/13/3, `INV-B:278` 5/14/3). Row counts in SPEC:81-92 (10), SPEC:97-125 (27) and SPEC:131-137 (6) are correct.
- Not covered: the content of any `src/` file, so no claim about what a command file really says was re-verified.

## Expert panel (critique mode; focus requirements and architecture)

Sequence run: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard (architecture, reliability); Whittaker (adversarial, always active, `command.md:83`); Newman, Hohpe (architecture focus). Crispin, Gregory and Hightower are outside the two focus panels (`command.md:133,144`).

## Findings by grade

No finding met the blocking bar. Each Medium finding below needs a guess about which reading an implementer picks, or restates a requirement the spec never states. Per `...prompts.md:31` they are Medium and listed under follow-up candidates even where the label would be MAJOR. There are no CRITICAL findings.

=== REQUIREMENTS ANALYSIS ===

**M-1 (Medium; Wiegers, Adzic): the P1 acceptance test requires an `## Unattended mode` section on commands whose gates are only resolved in P4.**
- SPEC:159 has P1 accept `--unattended` on every command in 3.1 and 3.2 except `/sc:load`, "a no-op where a command has no gate". SPEC:195 (AC-1.1) requires the section on each of them.
- `implement`, `post-release` and `pr-submit` have gates (SPEC:109,113,114) that SPEC:162 defers to P4 pending D2-D4 (SPEC:154,225).
- A P1 implementer who follows the text adds a section and flag to those three commands that promise unattended behaviour, which contradicts WC-2 (SPEC:60) until P4. A worker dispatched with that flag in P1-P3 would still stall on `E-HALT-QA`, the `[y/n]` at `--monitor 1` or the post-release confirmations.
- It needs a guess whether P1 intends a stub. The spec never says what the flag does for gated commands before their phase, nor that the coordinator must not dispatch them yet.
- Recommendation: state in P1/AC-1.1 that the three P4 commands are excluded until P4, or that the P1 section for them says "gates not yet resolved, do not dispatch".

**M-2 (Medium; Wiegers): `WC-3` allows an `ask`, while `AC-2.2` and `7.2` require the worker to end `failed` on a gate.**
- WC-3 (SPEC:61) says a worker that holds a preamble "may instead ask the coordinator once".
- AC-2.2 (SPEC:200) passes only on `worker_done --outcome failed` with `status: blocked`.
- 7.2 step 3 (SPEC:182) waits for `worker_done,escalation,question` and expects exactly one `worker_done`.
- A worker that follows WC-3 raises a `question` and the AC-2.2 pass condition is not met. The "may" is unresolved: the spec does not say whether the acceptance runs forbid `ask`, or what a passing run looks like when the coordinator answers.
- Recommendation: add to AC-2.2 whether the test brief forbids `ask`, or give the alternate pass path.

**M-3 (Medium; Adzic, Wiegers): no requirement for a missing output directory under `--unattended`.**
- WC-4 (SPEC:62) locates the contract in `<output-dir>`, "the directory the coordinator passed". WC-2(c) (SPEC:60) resolves a gate as blocked by writing that contract.
- If the coordinator omits the output flag, or the path cannot be created, there is nowhere to write it. Nothing says whether the command refuses before any work in chat only, or picks a default path.
- WC-5 (SPEC:63) covers only the worker-side result ("no report exists" is `failed`). The command-side requirement is missing.
- Section 2.3 (SPEC:73) puts the duty on the coordinator but states no command behaviour. This is a requirement the document never states, not stated text that does harm.

**M-4 (Medium; Cockburn, Adzic): `fresh dir` resume (WC-6) is not reconciled with a contract path fixed before dispatch (WC-4).**
- About 20 rows in 3.2 say "fresh dir" for WC-6 (for example SPEC:99-101). WC-6 (SPEC:64) says the command "writes each run into a fresh output directory".
- WC-4 requires the contract at the coordinator-passed directory. A fresh subdirectory created by the command would put the report where the coordinator cannot know it.
- The workable reading is that the coordinator passes a new `<output-dir>` on `--retry-of`. Section 2.3 (SPEC:73) does not say so, and 7.2 never tests a retry.
- This also matters for WC-3 re-invocation after an `ask`: re-running a fresh-dir command into the same directory has undefined effect on the earlier `blocked` contract.

**M-5 (Medium; Whittaker, Wiegers): the `3.1` "brief must pass" column and the `2.3` rule disagree on `--unattended` before P1.**
- Section 2.3 (SPEC:73) says the brief states the exact command line "including `--unattended`".
- The P0 smoke commands (SPEC:158,194) and the 3.1 column "Brief must pass" (SPEC:82-92) omit it. The flag does not exist until P1 (SPEC:159).
- AC-0.4 therefore tests a different invocation than the contract describes. It is minor in effect but it makes the P0 result not transfer to later phases.

**M-6 (Medium; Wiegers): `tdd` and `release-split` gate triggers are judged, not defined.**
- SPEC:90 resolves "topic-only clarification" as blocked and SPEC:200 tests it with `"auth"`.
- "Precise component prompt, not a bare topic" has no testable boundary (a two-word prompt versus one sentence). Two implementers will place the gate differently. The same applies to "spec-shaped input" (SPEC:89).

**N-1 (minor; Wiegers): wording gaps.**
- WC-1 says the fallback must be "well inside" the 60 s limit (SPEC:59). The evidence line cited says about 45 s fails and 30 s passes (`CAPS:49` quotes `EVIDENCE.md:45,56`). The spec could state 30 s as the tested value.
- The contract schema has no version field or timestamp (SPEC:62), unlike the workflow contract "contract 1.1" it models (`INV-B:272`).
- SPEC:159 lists the small ready-command fixes as "adversarial, cleanup-audit, index-repo, workflow" and omits the `init-lite` P1 contract fix that SPEC:87 assigns to P1.
- `README:31` is cited as the basis for WC-9 (SPEC:67) and for the `/sc:git` row (SPEC:133). It is a rule for this planning run's workers, not a repository rule for commands. The `/sc:git` evidence is better carried by `INV-A:91`.

=== ARCHITECTURE ANALYSIS ===

**M-7 (Medium; Fowler, Nygard): the `tasklist` resolution contradicts the inventory evidence it cites.**
- SPEC:122 has Stage 10.5 pass `--unattended` to each nested reflect "so the headless rule applies".
- Per `INV-B:109`, the headless rule auto-accepts remediation "for auto-fixable registers and skips the gates". Per `INV-B:46,215`, Stage 10.5 passes `--remediate`. The inventory's recommended change is to drop `--remediate` in 10.5, and to run the reflect fan-out "at the worker's top level, not inside subagents".
- The spec keeps `--remediate`, relies on auto-accept, and says the fan-out is "one layer below the worker, inside Claude Code's nesting limit" (SPEC:122, citing `INV-A:14`).
- An implementer who follows SPEC:122 builds an unattended tasklist run in which N nested reflects each auto-accept a hand-off to `sc:workflow` or task-builder. That is more work than the brief authorised, and the spec never says what scope it has. Whether auto-accept fires for these registers is UNVERIFIED (`INV-B:322`, "who answers the reflect remediation offer").
- The residual risk is a guess about which behaviour fires, so it is Medium.
- Recommendation: state that tasklist `--unattended` drops `--remediate`, as `INV-B:215` recommends, or justify the divergence.

**M-8 (Medium; Fowler, Newman): `AC-C1` can fail on text the spec itself permits.**
- SA-2 (SPEC:147) permits one Orca mention in a changed command, "as an example of a caller's question channel inside the contract file". SA-5 (SPEC:150) adds an Orca section to `HOW-WE-WORK.md`.
- AC-C1 (SPEC:172) greps `src/superclaude/core` for `orca(-ide) (orchestration|worktree|terminal|agent)` and requires no output. Both new files are in `core/` (SPEC:52,158).
- An example such as `orca orchestration ask`, or a routing line such as `orca worktree create`, would make AC-C1 fail in P0. The implementer has to guess the permitted wording. The baseline is clean (`E5`, SPEC:25, UNVERIFIED here).
- Recommendation: exempt the two files from AC-C1, or state the permitted wording in SA-2.

**N-2 (minor; Hohpe): contract-file name collisions are not discussed.**
- Several commands write `<output>/return-contract.yaml` (`reflect`, `brainstorm`, `workflow`, `adversarial`: SPEC:83-84,88,92). Several others now also would, and a command that invokes another can share an output directory with it (for example `workflow` Wave 4 invokes reflect, `INV-B:271`).
- The spec does not say who wins when two contracts target one path. Whether this occurs is UNVERIFIED.

**N-3 (minor; Newman): `validate-roadmap` has two report names and no decision.**
- SPEC:124 says "reconcile" and that the coordinator dispatches `superclaude roadmap validate` until then. P3 is where the choice gets made, but AC-3.1 (SPEC:204) only checks that both files name the same filename, not which.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

All findings use the command's template; severity is by consequence.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / WC-2(c) (SPEC:60,62)** fails when **`--unattended` is passed with no output flag**. Concrete attack: before, the brief is `/sc:analyze src --unattended`, no `--output`, no contract. After, the gate resolves as blocked, so the command must write a contract to a directory it does not have. The result is no file, and WC-5 ends the run `failed` with nothing to read. Graded **M-3** (Medium).
2. I can break this specification by **Sequence Attack**. The invariant at **WC-3 / WC-6 (SPEC:61,64)** fails when **a fresh-dir command is re-invoked after an `ask` answer into the same output directory**. Concrete attack: run 1 writes `return-contract.yaml` with `status: blocked` into `<dir>`. The answer arrives and run 2 starts "fresh". Either it overwrites the blocked contract, or it creates a subdirectory the coordinator does not know. Graded **M-4** (Medium).
3. I can break this specification by **Divergence Attack**. The invariant at **WC-3 versus AC-2.2 (SPEC:61,200)** fails when **the worker holds a preamble and chooses `ask`**. Concrete attack: the worker asks, the coordinator answers, and the run ends `succeeded`. AC-2.2 expects `failed`. Graded **M-2** (Medium).
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (SPEC:63)** fails when **a command's own status vocabulary uses `blocked` or `partial` with another meaning**. Concrete attack: `cli-portify` carries `resume_phase` fields and `user_rejected` (`INV-A:45`); mapping a user-rejected approval to `blocked` versus `failed` is unspecified. The spec says "commands that already write a contract keep their fields and add the missing ones" but not how the old status maps. Not a wrong outcome by itself, so a **minor note (N-4)**.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (SPEC:68)** fails when **a command has many sequential 4-minute waits**. Concrete attack: `cli-eval` evals run up to 3600 s (`INV-A:65`), which is 15 splits, each needing a heartbeat; the spec sets no ceiling on total run time and records that Orca's bound is UNVERIFIED (SPEC:282). Inference is possible, so minor (**N-5**).

## Guard Condition Boundary Table

Trigger: the spec contains threshold and boolean guards, so the table is produced (`command.md:313`). The spec's own "guards" are rules in prose, so each row is one guard and the class is chosen where it can occur; classes that cannot occur are left out with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| output-dir known (WC-4) | SPEC:62 | Zero/Empty | no `--output`/`--output-dir` | false | not specified (M-3) | GAP |
| output-dir known (WC-4) | SPEC:62 | Typical | `--output <dir>` | true | contract at `<dir>/return-contract.yaml` | OK |
| report exists (WC-5) | SPEC:63 | Zero/Empty | no report file | n/a | `--outcome failed` | OK |
| status mapping (WC-5) | SPEC:63 | Legitimate Edge Case | `partial`, or FAIL verdict audit | n/a | `succeeded`, body states status | OK |
| status mapping (WC-5) | SPEC:63 | Sentinel Value Match | legacy status such as `user_rejected` | n/a | not specified (N-4) | GAP |
| readiness 60 s (WC-1) | SPEC:59 | Maximum/Overflow | fallback 45 s or more | fails | tested at 30 s fallback; "well inside" untested (N-1) | OK |
| depth 1 (WC-8, R1) | SPEC:33,66 | Maximum/Overflow | worker calls `worker-start` | refused | forbidden and refused with `nested_worker_depth_exceeded` | OK |
| wait 4 min (WC-10) | SPEC:68 | Maximum/Overflow | single wait over 4 min | true | split into waits of at most 4 min | OK |
| wait 4 min (WC-10) | SPEC:68 | Zero/Empty | no wait in command | n/a | no change | OK |
| `--unattended` on a gated P4 command | SPEC:159,162 | Typical | `/sc:implement ... --unattended` in P1-P3 | n/a | flag accepted, gate unresolved (M-1) | GAP |
| `ask` allowed (WC-3) | SPEC:61 | Divergence | gate hit with a preamble | n/a | "may ask"; AC-2.2 expects failed (M-2) | GAP |
| resume vs fresh dir (WC-6) | SPEC:64 | One/Minimal | retry into same dir | n/a | not specified (M-4) | GAP |
| `--retry-of` circuit breaker | SPEC:64 via CAPS:116 | Maximum/Overflow | three failed starts | trips | Orca owns; a worker's own `failed` does not count (SPEC:263) | OK |
| confidence below 0.70 (task) | SPEC:121 | Sentinel Value Match | exactly 0.70 | false | "below 0.70" blocks, so 0.70 proceeds | OK |

Left out, with reasons: the `--monitor 1` guard (a flag, not a numeric class; refused, SPEC:114); the heartbeat cadence of 5 minutes (comes from the dispatch preamble, `CAPS:130`, not a spec guard).

GAP cells: 5. Each was graded under FR-8/FR-9 (`command.md:332-333`): none names a concrete wrong outcome without a guess about the implementer's reading, so each is Medium and appears under follow-up candidates. No blank "Specified Behavior" cell exists other than the GAP cells.

## Pipeline Dimensional Analysis

The spec describes staged rollout, not a data pipeline. The stage counts do conserve at the command level: 43 commands = 10 ready + 27 changing + 6 coordinator-only (SPEC:76; `INV-A:73`, `INV-B:278`). Phase membership in SPEC:159-162 gives P1 9 (3.2 rows) + 4 ready fixes, P2 15, P3 4, P4 3. The only count mismatch is that `init-lite` is missing from the P1 fix list (N-1), which loses no command. The 36 flag-accepting commands in P1 (43 - 6 - `load`) do not all get a complete mode until P4 (M-1). This is a Medium consistency issue, not a CRITICAL count mismatch, because no downstream consumer assumes an unfiltered count.

## Quality assessment (0-10)

- Clarity 8: decisions, evidence and rejected alternative are laid out and traceable.
- Completeness 7: M-1, M-3, M-4 are gaps.
- Testability 8: nearly every requirement has an AC with a pass condition. M-2 and M-8 are exceptions.
- Consistency 7: M-1, M-2, M-5, M-7, M-8 are internal tensions.

## Follow-up candidates (Medium and minor; none triggers a revision)

- M-1 P1 flag semantics for the three gated P4 commands (SPEC:159,162,195).
- M-2 `ask` permitted by WC-3 versus AC-2.2 and 7.2 step 3 (SPEC:61,182,200).
- M-3 missing output-dir behaviour under `--unattended` (SPEC:60,62).
- M-4 `fresh dir` versus contract path fixed before dispatch (SPEC:62,64,73).
- M-5 `--unattended` in 2.3 versus the P0 smoke commands (SPEC:73,194).
- M-6 undefined "bare topic" and "spec-shaped" boundaries (SPEC:89,90,200).
- M-7 `tasklist` Stage 10.5 diverges from `INV-B:215` (SPEC:122).
- M-8 `AC-C1` versus SA-2/SA-5 wording (SPEC:147,150,172).
- N-1 "well inside", no contract version, `init-lite` missing from P1 list, `README:31` used as repository rule.
- N-2 contract-file path collisions.
- N-3 `validate-roadmap` filename choice.
- N-4 legacy status mapping (`cli-portify` and similar).
- N-5 no ceiling on total run time for sliced waits.

The session that ran this review has no user to ask, so the once-per-loop question about opening an issue for these items is left to the coordinator (`command.md:260`); no issue was created.

## Strengths worth keeping (not findings)

- The evidence-strength section states its own gaps plainly (SPEC:41-45), including that PR #329 proves the nested route and not the direct one.
- Citations to the inventories are accurate in every case I could check, and the 10/27/6 counts reconcile.
- SA-1 to SA-6 keep standalone behaviour explicit, and the open decisions D1-D5 each carry a recommendation.

## Reviser brief

No blocking finding is open, so there is nothing to revise. A reviser must not edit for M-1 to M-8 or N-1 to N-5. For the record, the reviser contract (`command.md:263`) is: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, with bytes added and deleted per finding id. A brief may narrow this scope and may not widen it or regrade a minor or Medium finding as blocking, including through "apply all findings" (`command.md:264`). No brief clause was overridden in this run.

verdict: PASS
