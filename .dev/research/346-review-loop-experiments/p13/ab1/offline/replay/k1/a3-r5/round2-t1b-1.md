review: 2 of 3

# Spec-panel critique, round 2 (re-review): Orca worker-contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:34-47` (read in full before this review). Roles as the table at `:38-42` fixes them: CANDIDATE = the `@file`, BASELINE = `--baseline`, PRIOR = `--re-review`.
- CANDIDATE `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`: sha256 `5d3d225a6ef33d0f0c3eb9b745dd4e780b4ca5a0b2dd745dd00ce966449d2b61` (58448 bytes, 285 lines)
- BASELINE `.dev/orca-command-refactor/specs/history/spec-v1.md`: sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes, 285 lines). This hash equals the candidate hash recorded in the prior report's header (`round1.md:8`), so the baseline is the text round 1 reviewed.
- PRIOR `.dev/orca-command-refactor/review/round1.md`: sha256 `5e785003d1107616a2d2c3a3ecd2e6ab5d417f31d5bef4b62a0e31f77e224bc3`; its header is `review: 1 of 3` (`round1.md:1`), so N = 2. Its last line is `verdict: FAIL` (`round1.md:197`) and it is not at `review: 3`, so the review runs.
- reviewer model actually used: `claude-sonnet-5-5`
- Mode: critique, re-review. The Improve step is skipped and no revised specification is written (`--re-review` ignores `--iterations`). Nothing but this file was written. No brief clause was overridden.
- Citation key: `S:N` = line N of the candidate (the candidate and baseline have the same line numbers for every changed line); `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `R1:N` = line N of the prior report; `command.md:N` = the `/sc:spec-panel` definition given to this run.
- `rf-qa.md` (project `.claude/agents/rf-qa.md`, else `~/.claude/agents/rf-qa.md`): not present in the sandbox (both paths checked), so the Fix Cycle steps 1-5 it defines were not read. The re-check of each prior blocker follows the rules of `command.md:262` and the RE-REVIEW prompt, which stand alone.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md`. It reports 16 changed lines in 6 hunks (lines 73, 76, 159, 176, 193-196; the bare number is the same in both files). Lines copied verbatim.

### BEFORE (baseline)

```text
73:  The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76:  The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
159: | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
176: | AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep -E '^-[^-]'` | prints nothing: edits are additive |
193: | P0 | AC-0.3 | `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \| grep -E '^-[^-]'` | prints nothing: no existing routing row changed (SA-5) |
194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
196: | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

### AFTER (candidate)

```text
73:  The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` once the command's phase has landed (F-1) and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76:  The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every command changed for unattended mode (not load, whose P1 change is its usage line) also gains the `## Unattended mode` section (section 2.1) in its own Phase, not earlier (F-1). Phase numbers refer to section 6.
159: | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by the commands in the next column only (a no-op where a command has no gate; a command first accepts the flag in the phase that converts its gates, F-1); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
176: | AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep -E '^-' \| grep -v '^--- a/'` (F-3: lists deleted bullets, which start `--`) | prints nothing: edits are additive |
193: | P0 | AC-0.3 | `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \| grep -E '^-' \| grep -v '^--- a/'` (F-3) | prints nothing: no existing routing row changed (SA-5) |
194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass as written. Steps 3 and 4 use the command's existing report file, because no P0 edit makes a command write the WC-4 path (F-2): troubleshoot `REPORT.md`, workflow its `.dev/tasks/to-do/<id>/return-contract.yaml`, adversarial its existing contract (filename unfixed until P1) (`INV-B:242,272`; `INV-A:60`). Step 3: `--outcome` matches that file's own verdict and `--report-path` names it. Step 4: `test -s` on it only. Record the results in the phase report; a failure here reopens section 1 |
195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in the P1 row of section 6 except load (F-1) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
196: | P1 | AC-1.2 | 7.2 live check on each P1 command except load (F-1) with `--unattended --output <dir>` | all steps pass |
```

Whitespace-only differences: none found (`diff` without `-w` reports the same 16 lines). Size: 57763 to 58448 bytes (+685).

### Self-check (run)

`grep -nF` of each of the 8 AFTER lines (without `>`) in the candidate found each at the line shown above (73, 76, 159, 176, 193, 194, 195, 196); `grep -nF` of each of the 8 BEFORE lines (without `<`) in the baseline found each at the same line numbers. No quote was missing, so the roles are not swapped.

## Input detection

The input is a spec (not a TDD, not a PRD), as in round 1 (`R1:20-22`); steps 6a-6d do not apply.

## Coverage

Covered: all 285 lines of the candidate (the diff touches 8 of them); the prior report in full; `README.md`; the inventory lines the changed text cites (`INV-A:35,60`, `INV-B:242,272`: each says what AC-0.4 claims). Prior blocking findings were re-checked against the AFTER text only. I ran two shell tests of the new `grep` pattern (below). Lines not changed by the revision were read for dependencies on the changed lines and were not re-reviewed as a whole: assurance is scoped to changed lines plus prior blockers.

Not checkable: every citation to a file outside `.dev/orca-command-refactor/` (`src/superclaude/...`, `CLAUDE.md`, `HOW-WE-WORK.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`) is UNVERIFIED here. No finding below rests on such a file alone.

Panel (review order `command.md:103-113`): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture and adversarial); Crispin (check completeness). Gregory and Hightower: no finding.

## Prior blocking findings

| ID | Prior status | Status now | Basis (AFTER text only) |
|---|---|---|---|
| F-1 | open, blocking (`R1:34-46`) | **resolved** | S:159 now limits the `--unattended` flag to "the commands in the next column only" and says "a command first accepts the flag in the phase that converts its gates". S:76 gives each changed command its `## Unattended mode` section "in its own Phase, not earlier". S:195 (AC-1.1) now quantifies over "the P1 row of section 6 except load", not "sections 3.1-3.2", and S:196 (AC-1.2) likewise. Re-check of the three collisions: (1) auggie-review is a P2 command (S:100, S:160), so after P1 it does not accept the flag, which removes the state where the flag exists but the default posting is on; implement, post-release and pr-submit are P4 (S:109, S:113, S:114, S:162), so the same holds; (2) load is excluded from AC-1.1 and AC-1.2, so the test no longer needs a contract file for it (S:112); (3) pr-submit is not in the P1 row, so AC-1.1 no longer requires an unattended section that D3(a) (S:240) says it must not get. Count check: the P1 flag scope now names the 13 commands of the P1 command column (9 gate-free incl. load, 4 fixes; counted against S:99-125 rows marked P1 and S:159); see the Quantity Flow Diagram. |
| F-2 | open, blocking (`R1:47-58`) | **resolved** | S:194 (AC-0.4) now says steps 3 and 4 "use the command's existing report file" for the three smoke commands and names each: troubleshoot `REPORT.md`, workflow `.dev/tasks/to-do/<id>/return-contract.yaml`, adversarial "its existing contract (filename unfixed until P1)". The citations check: `INV-B:242` says the troubleshoot report path is REPORT.md and `return-contract.yaml` only with `--caller task-unified`; `INV-B:272` gives the workflow path; `INV-A:60` says the adversarial contract filename is not fixed and has been written at two paths. Step 3 is now "`--outcome` matches that file's own verdict and `--report-path` names it", step 4 is `test -s` only. So the check no longer asks for a WC-4 path (S:62) that P0 cannot produce, and the "reopens section 1" clause (S:194) no longer fires from an internal inconsistency. Residual wording issue: R2-M2 (Medium). |
| F-3 | open, blocking (`R1:59-66`) | **resolved** | S:176 and S:193 now use `grep -E '^-' \| grep -v '^--- a/'`. Tested on a synthetic diff body (`diff --git`, `--- a/x.md`, `+++ b/x.md`, then `-- Will Not: modify specs`, `-Plain removed line`, `----`, `+new`, `-/sc:foo [--a]`): the new pipe printed all four removed lines (the deleted bullet, the deleted prose line, the deleted `---` rule shown as `----`, the deleted usage line) and not the `--- a/` header; the old pattern `^-[^-]` on the same input printed only the prose line, confirming the round-1 defect. A deleted bullet therefore makes AC-C5 print, so AC-C5 fails as intended. Remaining edge cases are Medium or minor: M-12 (below), and a deleted line whose own text starts `-- a/` would be hidden (negligible). |

No finding regressed. No prior blocking finding was deferred or withdrawn.

## Findings on changed lines

Grading used: for a blocking finding the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" had to hold with no further assumption. None of the findings below meets that bar; each needs a guess about which reading the implementer or coordinator picks, or is a requirement the document never states, so each is Medium or minor and sits under `follow-up candidates`.

### Blocking findings (0)

None.

### Medium findings on changed lines (warnings, follow-up candidates)

- **R2-M1. AC-1.1 and AC-1.2 now reach the four fix-only commands of the P1 row, whose section 3.1 rows state neither an unattended section nor a WC-4 contract change.** origin=changed (S:195, S:196 "the P1 row of section 6 except load"); the inherited rows are unchanged. The P1 row lists `adversarial, cleanup-audit, index-repo, workflow` (S:159). Their rows (S:83, S:85, S:86, S:92) name only a filename, report-location or pre-creation-STOP fix, and cleanup-audit and index-repo report to fixed paths (`.claude-audit/pass<N>-summary.md`, `PROJECT_INDEX.md`, S:85-86). S:195 requires each to have a section "naming `return-contract.yaml`", and S:196 runs step 3 of 7.2 on each with `--unattended --output <dir>`, where the report path must be the WC-4 contract path `<output-dir>/return-contract.yaml` (S:62, S:182). S:79 says the worker "reports the named file until Phase 1 adds the contract", which supports the reading that P1 adds it, but S:79 also says "the only command changes are the small fixes". Which reading wins is not stated; either reading is harmless (an extra section; a contract file) and the failure shows in the first P1 live check, so this is Medium. It is the round-1 M-1/M-4 gap (contract location where there is no coordinator-passed directory, `R1:71,74`) now sitting under a changed acceptance check. UNVERIFIED: whether workflow and cleanup-audit accept an `--output` directory at all (the inventories do not say). Experts: Crispin, Wiegers.
- **R2-M2. AC-0.4 step 3 matches the outcome to "that file's own verdict", but two of the three files have no stated verdict field.** origin=changed (S:194). `INV-B:242` names `report_path` (REPORT.md) and, for troubleshoot, no status or verdict field; the adversarial contract's fields are not listed in `INV-A:35,60`. Only workflow's contract is known to carry `status` (`INV-B:272`). An implementer must read the report to decide "failed" or "succeeded"; WC-5 (S:63) maps from the report's `status`. Fix on follow-up: say the P0 coordinator reads the report and judges. Experts: Adzic, Wiegers.
- **R2-M3. "once the command's phase has landed" (S:73) has no meaning for commands that have no phase.** origin=changed. Section 3.1 commands with no fix (brainstorm S:84, init-lite S:87) appear in no phase row (S:158-162), and pr-submit under D3(a) gets no change (S:240). The coordinator therefore never passes `--unattended` to them, which is safe for these commands (they have no gate in the spec), but then WC-4 ("in unattended mode the command writes `<output-dir>/return-contract.yaml`", S:62) never applies to init-lite, whose report is a markdown file (S:87). The text does not say that such a command is simply run with its stated flags. Experts: Wiegers, Cockburn.
- **R2-M4. After the F-1 fix nothing in S:73 or section 3 says a section 3.2 command must not be dispatched before its phase lands.** origin=changed (S:73, S:159). Section 3.1 says its commands "run as workers now" (S:79); section 3.2 is titled "Needs a change" and the phase rows say when each is converted (S:160-162), but the rule is implied. A coordinator that follows S:73 literally for auggie-review before P2 omits `--unattended` (the flag is not yet accepted), and the command posts to GitHub by default (S:100; `INV-A:38`). Whittaker's sequence attack, attempted against the new text: P1 passes; the coordinator dispatches `/sc:auggie-review 123 --output-dir <dir>` as a worker; the PR review is posted. This needs a coordinator that dispatches a command the spec calls not ready, so it is Medium, not blocking. Narrow fix on follow-up: one sentence in S:73 or S:76 saying a section 3.2 command is dispatched only after its phase. Experts: Whittaker, Nygard.
- **R2-M5. M-12 carried, with the new pattern.** origin=changed (S:176). The new AC-C5 pattern prints every removed line, as intended. A phase that documents the new `--unattended` flag by editing an existing Usage line changes that line, so it prints, and SA-4 (S:149) calls flag additions "additive". Same defect as round 1 M-12 (`R1:82`), same grade: SA-4 allows a new section as the place for the flag, so an implementer can avoid it.

### Minor notes

- Whether `load` accepts `--unattended` is unstated: S:159 lists it in the flag's command column ("accepted by the commands in the next column only") while S:76, S:195 and S:196 exclude it from the section and live checks. No wrong outcome (load has no gate, S:112).
- A deleted line whose own text begins `-- a/` is hidden by `grep -v '^--- a/'` (S:176, S:193); negligible.
- S:194 is now a long single table cell; it reads correctly but is hard to scan.

## === REQUIREMENTS ANALYSIS ===

- **Wiegers (lead).** Each of the three revisions is consistent with the requirement it serves: WC-9 and WC-2 (S:60, S:67) can no longer be contradicted by P1 (S:159), and AC-1.1 now has a stated domain (S:195). Remaining gaps are traceability from the four fix-only commands to the section (R2-M1) and phase-less commands (R2-M3).
- **Adzic.** The P0 example is now runnable per command with a named file (S:194); "that file's own verdict" lacks a concrete example for REPORT.md (R2-M2).
- **Cockburn.** Who dispatches what, and when, is clearer (the coordinator waits for the phase, S:73); the "must not dispatch early" rule is implied rather than stated (R2-M4).

## === ARCHITECTURE ANALYSIS ===

- **Fowler (lead).** The interface (flag) and the behaviour that makes it safe (gate conversion) are now introduced in the same phase for every phase-bearing command (S:76, S:159); the round-1 structural weakness is gone. The boundary (Orca above, commands as units) is untouched by the diff.
- **Newman.** Versioning order improved: a command exposes the flag only when it honours it. Open question for later phases only: what a command does if handed an unknown `--unattended` early (not stated; the coordinator is told to omit it, S:73).
- **Hohpe.** No lifecycle-message wording changed; S:61-65 and S:70 stand. P0 step 3 now compares `--outcome` with a file that is not the contract (S:194); the exactly-once rule (S:63) is unaffected.
- **Nygard.** Failure modes: the early-dispatch case (R2-M4) is the only new hole; AC-C5 now fails closed on deletions, which strengthens the standalone guarantee (SA-1, SA-4).

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Template per `command.md:82`. All five methodologies were applied to the changed lines; only attacks that found something are listed.

1. I can break this specification by **Sequence Attack**. The invariant at **S:73 with S:159-160** fails when **a coordinator dispatches a section 3.2 command before its phase lands**. Concrete attack: (before) P1 passed, auggie-review still in section 3.2 with P2 pending; (step) the coordinator builds the brief per S:73 and omits `--unattended` because "the command's phase" has not landed; (after) the worker runs the command with today's defaults and posts the review. Maps to R2-M4 (Medium: needs a coordinator that ignores the "Needs a change" title).
2. I can break this specification by **Zero/Empty Attack**. The invariant at **AC-C5, S:176** fails when **the diff is empty or only a header exists**. Concrete attack: (before) no change; (after) `git diff -U0` prints only `--- a/...` and `+++ b/...`; the pipe prints nothing; the check passes, which is correct. Not a defect; the same attack against the old pattern is the F-3 defect, now closed.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:176** fails when **a deleted line's text starts `-- a/`**, because the exclusion `^--- a/` treats it as a header. Concrete attack: (before) a line `-- a/foo` in a command file; (after) it is deleted; the diff line is `--- a/foo`; the pipe hides it. Negligible (minor note above).
4. I can break this specification by **Divergence Attack**. The invariant at **S:194 step 3** fails when **the three smoke commands end in different ways**: troubleshoot (a report file with no status field, R2-M2), workflow (a contract with `status`), adversarial (a contract whose path varies, `INV-A:60`). The text gives one rule ("that file's own verdict") for three different shapes. Medium: R2-M2.
5. I can break this specification by **Accumulation Attack**. No accumulation point on the changed lines (counts of commands are conserved, see the Quantity Flow Diagram).

## === GUARD CONDITION BOUNDARY TABLE ===

Trigger: the changed lines contain threshold checks, quantifiers and a boolean guard (the grep gates, the phase gate on the flag, the AC-1.1 test domain, the AC-0.4 step relaxation), so the table is produced (`command.md:313`). In a re-review it covers guards on changed lines only (`command.md:262`). Construction: Nygard; completeness: Crispin; attack: Whittaker. Guards: G-6 AC-C5 and AC-0.3 diff gate (S:176, S:193); G-9 flag acceptance by phase (S:73, S:159); G-10 AC-1.1 test domain (S:195, S:196); G-11 AC-0.4 steps 3 and 4 (S:194). G-6 keeps its round-1 number.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G-6 diff gate | S:176 | Zero/Empty | no removed lines (headers only) | prints nothing | pass | OK |
| G-6 diff gate | S:176 | One/Minimal | one removed prose line `-Plain removed line` | prints it | fail | OK |
| G-6 diff gate | S:176 | Typical | one removed bullet `-- Will Not: ...` | prints it (tested) | fail (round-1 F-3 closed) | OK |
| G-6 diff gate | S:176 | Sentinel Value Match | removed line whose text starts `-- a/` | hidden by `grep -v '^--- a/'` | pass (wrong) | GAP (minor, negligible) |
| G-6 diff gate | S:176 | Legitimate Edge Case | `[--unattended]` added to an existing Usage line | prints the old Usage line | fail although SA-4 calls it additive | GAP (Medium, R2-M5 / M-12) |
| G-6 routing gate | S:193 | Typical | removed routing row `-\|...` | prints it | fail (SA-5) | OK |
| G-9 flag by phase | S:73, S:159 | Zero/Empty | command in no phase (brainstorm, init-lite) | no flag passed | run with stated flags, behaviour not stated | GAP (Medium, R2-M3) |
| G-9 flag by phase | S:73, S:159 | Typical | P1 command, P1 landed | flag accepted | unattended mode | OK |
| G-9 flag by phase | S:73, S:159 | Legitimate Edge Case | section 3.2 command, phase not landed (auggie-review before P2) | flag not passed | today's defaults, outward default on; dispatch before the phase is not forbidden in words | GAP (Medium, R2-M4) |
| G-9 flag by phase | S:73, S:159 | Sentinel Value Match | load, in the P1 flag column | flag accepted or not: unstated | no gate, no effect | GAP (minor) |
| G-10 AC-1.1 domain | S:195 | Zero/Empty | section-4 command | no section | test asserts none | OK |
| G-10 AC-1.1 domain | S:195 | Typical | analyze (P1) | section present | test passes | OK |
| G-10 AC-1.1 domain | S:195 | Legitimate Edge Case | load, excluded | no section required | OK (the round-1 contradiction is gone) | OK |
| G-10 AC-1.1 domain | S:195, S:196 | Legitimate Edge Case | fix-only commands in the P1 row (adversarial, cleanup-audit, index-repo, workflow) | section and live check required | rows state no section or contract change | GAP (Medium, R2-M1) |
| G-10 AC-1.1 domain | S:195 | Sentinel Value Match | pr-submit under D3(a) | not in the P1 row | not tested (round-1 F-1 closed) | OK |
| G-11 AC-0.4 | S:194 | Typical | workflow `status` in its own contract | outcome compared | defined | OK |
| G-11 AC-0.4 | S:194 | Legitimate Edge Case | troubleshoot `REPORT.md`, adversarial contract: no stated verdict field | comparison undefined | "that file's own verdict" | GAP (Medium, R2-M2) |
| G-11 AC-0.4 | S:194 | Zero/Empty | step 4 file missing or empty | `test -s` fails | fail | OK |

Classes left out: Maximum/Overflow for every guard here (each guard takes a state, a set of names or a diff, not a quantity), and One/Minimal for G-9, G-10, G-11 (they test membership, not a count).

FR-8/FR-9 grading: every GAP row above is a missing or unstated requirement, not a stated text that causes harm with no further assumption, so each is Medium or minor (`command.md:332-333`). None blocks.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)

Trigger met: P1's flag scope and AC-1.1's test domain are stages whose counts differ from the 43-command source. Round 1 found a divergence of 37 versus 13 here (`R1:155-173`). After the revision:

```text
[43 commands in cmd/ (21 INV-A:3 + 22 INV-B:3)] --> [Classification (S:76)] --> [10 ready (S:78)] [27 needs change (S:94)] [6 coordinator-only (S:127)]  (10+27+6 = 43: conserved)
[P1 row of section 6 (S:159)]: 9 gate-free (analyze, build, business-panel, design, document, explain, index, test, load) + 4 fix-only (adversarial, cleanup-audit, index-repo, workflow) = 13 named
   |--> [P1 flag scope (S:159): "the commands in the next column only" = 13]            consistent
   |--> [AC-1.1 test domain (S:195): P1 row except load = 12]                           consistent (load excluded, S:76)
   |--> [AC-1.2 live checks (S:196): P1 row except load = 12]                           consistent
   |--> [AC-1.1 negative assertion: section-4 commands = 6, none carry a section]       consistent
[section 3.2 rows by phase (S:99-125)]: P1 9 + P2 11 + P3 4 + P4 3 = 27 (conserved); [section 3.1 fixes by phase]: P1 4, P2 4 (reflect, release-split, tdd, troubleshoot), none 2 (brainstorm, init-lite)
[P2 row (S:160)]: 15 named = 11 (3.2) + 4 (3.1)   consistent
```

No remaining mismatch. The only count question is the 2 phase-less commands (R2-M3), which no stage consumes.

## Expert consensus and disagreements

- Consensus: the three revisions each close the finding they cite, with narrowing edits only (the revision added 685 bytes, 8 changed lines, no new section or rule). The decision and the requirement set are unchanged.
- Disagreement: Whittaker would grade R2-M4 blocking because the early-dispatch case reproduces the round-1 F-1 outcome by another route; Nygard and Fowler graded it Medium because the route needs a coordinator that dispatches a command the spec places in "Needs a change", and the spec's phase table already says when each is ready. Under the grading rule (a guess about which reading the actor picks) it stays Medium.

## Follow-up candidates

Medium and minor findings, none blocking, to be listed once for the user:

- New this round: R2-M1, R2-M2, R2-M3, R2-M4, R2-M5, and the three minor notes above.
- Carried unchanged from round 1 (`R1:67-87`): M-1 to M-16. The revision touched none of the lines they cite, except M-12 (now R2-M5). Their statuses are not re-graded here.
- Session handling: the session that ran this review should ask the user once for this loop whether to open an issue for these items. This run cannot hold a conversation, so no question was asked and no issue was created; the coordinator should ask once for this loop.

## Priority-ranked improvements

None required for the verdict. If the user wants a further edit, in order: R2-M4 (one sentence on early dispatch), R2-M1 (state whether the four fix-only commands carry the section and the contract), R2-M2 (name how P0 judges the outcome), then M-1, M-4, M-5, M-7 from round 1.

## Coverage statement

scoped PASS: changed lines + prior blockers

This is not whole-document assurance. A whole-document check would need a separate, labelled first review; its blockers would be escalated and would not start a fourth review (`command.md:262`).

## Reviser brief

Blocking finding ids: none. No revision is requested. (Rules, restated from the command's Review Loop bullet 6 for a coordinator who still revises: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each addition; prefer deleting or narrowing to adding; leave Medium and minor findings alone, including "apply all findings" requests. This brief lists no id, so nothing may be edited on the strength of this report.)

verdict: PASS


## Findings block

```findings-v1
{"prior": "L1", "status": "resolved"}
{"prior": "L1", "status": "resolved"}
{"prior": "L2", "status": "resolved"}
```
