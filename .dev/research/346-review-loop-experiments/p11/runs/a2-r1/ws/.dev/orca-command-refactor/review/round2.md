review: 2 of 3

# Spec-panel review, round 2 (re-review): `orca-worker-contract-spec.md`

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md        # CANDIDATE
  candidate_sha256: f42ebd1cb0922207da16c10e49e26f992ea80bee8c020e73ba1dacefbcfd5f95   # 285 lines, 58099 bytes
  baseline: .dev/orca-command-refactor/specs/history/spec-v1.md                        # BASELINE
  baseline_sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d   # 285 lines, 57763 bytes; equals the sha256 recorded in PRIOR (round1.md:8)
  prior: .dev/orca-command-refactor/review/round1.md                                   # PRIOR
  prior_sha256: 9123c145ce77fb5796e1f393bdb6d22a47c85b17686613a532b56ad5be980475
  review_date: 2026-11-10
  mode: critique
  re_review: true
  focus_areas: [requirements, architecture]
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Newman, Hohpe, Nygard, Whittaker]   # focus panels plus Whittaker (always active)
```

Citation key. `SPEC:N` = line N of the candidate. `BASE:N` = line N of the baseline. `R1:N` = line N of the prior report `review/round1.md`. `REV1:N` = line N of `review/revise1.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. Any citation to a file outside those is marked UNVERIFIED.

## What I covered

- Read in full: the README, PRIOR (214 lines), `revise1.md`, the whole CANDIDATE (285 lines), and the inventory lines the changed text cites (`INV-A:35,60-61,97`, `INV-B:31,57-65,112,237-245,267-275`, `CAPS:70-80`).
- Roles fixed by file value, not by reading order: CANDIDATE = the `@file`, BASELINE = the `--baseline` file, PRIOR = the `--re-review` file. The BASELINE sha256 equals the sha256 PRIOR recorded for the text it reviewed (`R1:8`), so BASELINE is the text round 1 saw.
- Ran `diff -w BASELINE CANDIDATE` (below): 5 changed lines, 0 whitespace-only changes, all in the lines `revise1.md` says it touched (`REV1:29-30`). The total byte change in `REV1:11-13` (57763 to 58099, +336) matches `wc -c` of the two files.
- Re-checked both prior blocking findings against the AFTER text only, then read the rest of the candidate for requirements that depend on the five changed lines (`SPEC:51`, `SPEC:62`, `SPEC:63`, `SPEC:73`, `SPEC:76`, `SPEC:79`, `SPEC:81-92`, `SPEC:99-125`, `SPEC:138`, `SPEC:149`, `SPEC:158-162`, `SPEC:167`, `SPEC:178-186`, `SPEC:265`).
- Per the Review Loop, the Guard Condition Boundary Table covers guards on changed lines only; findings on unchanged lines are minor notes unless they quote a changed line that depends on them.
- Not checkable here, so UNVERIFIED: every `src/superclaude/...` line citation not quoted by an inventory (for example `cmd/load.md:22,42-43,52,82` and the `REPORT.md` content of troubleshoot), the real `status` vocabulary of the adversarial and workflow contracts (`REV1:36` says the same), and the pass condition of every acceptance check (nothing was executed: no Orca, no repo). `rf-qa.md` is not present in the project or in the sandbox home, so the Review Loop bullet 5 rules stand alone.
- Did not edit the candidate or any other file, and started no other review.

### Grading applied
The Review Loop makes CRITICAL and FR-8/FR-9 findings blocking, and a MAJOR blocking only when it names a concrete wrong outcome an implementer would produce. Where a Guard Condition Boundary Table GAP generates an FR-8 finding, I apply the same test as the prior round (`R1:26`) under the Precedence bullet (a brief may narrow the blocking set): blocking only if "an implementer who follows the AFTER text as written builds X, and X is wrong because Y" holds with no further assumption. A GAP that is a requirement the text never states, or that needs a reading choice, is Medium and listed under follow-up candidates. This brief asks for concrete wrong outcomes, not a count, and lists Medium and minor under follow-up candidates. No GAP below passes the test.

## Step 1. Evidence block (`diff -w` BASELINE CANDIDATE)

Command: `diff -w .dev/orca-command-refactor/specs/history/spec-v1.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (exit 1, five hunks: `112c112`, `159c159`, `194,196c194,196`).

### BEFORE (baseline), lines starting `<`
```text
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

### AFTER (candidate), lines starting `>`
```text
> | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; it takes no `--unattended` and gets no `## Unattended mode` section or contract (B-2); separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `/sc:load` (B-2) (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; step 3 needs exactly one `worker_done` whose `--outcome` matches the status in the command's existing report (3.1 "Report today"), with that file as its report path; step 4 is `test -s` on that file; the contract arrives in P1 (B-1). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that neither `/sc:load` nor any section-4 command has one (B-2) | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `/sc:load` (B-2) with `--unattended --output <dir>` | all steps pass |
```

Line map: hunk `112c112` = load row of 3.2 (BASE:112 / SPEC:112); `159c159` = P1 scope row (BASE:159 / SPEC:159); `194,196c194,196` = AC-0.4, AC-1.1, AC-1.2 (BASE:194-196 / SPEC:194-196). Nothing else differs.

What changed, in words: AC-0.4 no longer requires steps 3 and 4 of the 7.2 live check in full at P0 (step 3 now matches the worker's outcome to "the status in the command's existing report", with that file as the report path; step 4 is `test -s` on that file); `/sc:load` is carved out of the P1 flag, AC-1.1 and AC-1.2; the load row says once that it takes no `--unattended` and gets no `## Unattended mode` section or contract.

## Re-check of prior blocking findings

Each prior blocking finding was judged against the AFTER text only, and against every requirement that depends on that text.

| Prior finding | Prior defect (`R1:92-102`) | Status | Decided from the AFTER text |
|---|---|---|---|
| B-1 AC-0.4 requires a step that Phase 0 cannot pass | Step 3 required the worker's report path to be "the WC-4 contract path" and its outcome to match the contract's `status` (SPEC:182), and step 4 parsed `d['status']` and `d['command']` (SPEC:183), while P0 makes no command edits (SPEC:158) and the contract arrives in P1. P1 could never start (SPEC:154). | **resolved** | AFTER `SPEC:194` replaces the requirement at P0: "steps 1, 2 and 5-7 pass; step 3 needs exactly one `worker_done` whose `--outcome` matches the status in the command's existing report (3.1 "Report today"), with that file as its report path; step 4 is `test -s` on that file; the contract arrives in P1 (B-1)". No P0 step now needs a contract or a YAML parse. Dependents agree: `SPEC:79` ("the worker reports the named file until Phase 1 adds the contract"), the 3.1 column "Report today" (`SPEC:81`, rows `SPEC:83`, `SPEC:91`, `SPEC:92`), `SPEC:158` (no command edits) and UNVERIFIED item 1 (`SPEC:272`, "Resolve: AC-0.4"). Steps 3 and 4 of 7.2 (`SPEC:182-183`) are unchanged, so P1 and later still use the full check, as `SPEC:196` requires. A Phase 0 run of the three named commands can now pass steps 1-7 as written; the residual looseness is follow-up M-14, not a gate that cannot pass. |
| B-2 AC-1.1 and P1 require a report contract for `/sc:load` | AC-1.1 asserted the section for "every command in sections 3.1-3.2" (SPEC:195), the P1 row gave load the flag (SPEC:159) and AC-1.2 ran the live check on each P1 command (SPEC:196), against the load row ("none (see note)", "not as its own Task", SPEC:112) and the Decisions row (SPEC:265). | **resolved** | AFTER `SPEC:112` says load "takes no `--unattended` and gets no `## Unattended mode` section or contract (B-2)"; AFTER `SPEC:159` limits the flag to "every command in sections 3.1 and 3.2 except `/sc:load` (B-2)"; AFTER `SPEC:195` asserts the section for every command "except `/sc:load`" and asserts "neither `/sc:load` nor any section-4 command has one"; AFTER `SPEC:196` runs the live check on each P1 command "except `/sc:load` (B-2)". The four lines now agree with `SPEC:112`, `SPEC:265` and `INV-B:65` ("writes no file"). The load usage-line fix stays (P1, `SPEC:149`, `SPEC:159`). The P1 command list still names "load (usage line only)", which is consistent with a usage-line edit and no flag. One general sentence, `SPEC:76`, was not edited; see M-15. |

No prior blocking finding is open or regressed. The diff is not empty, so the empty-diff rule does not apply.

## Guard Condition Boundary Table (changed lines only)

Trigger: the AFTER text adds three guards: the outcome-match condition and the `test -s` condition in AC-0.4 (SPEC:194), and the membership condition "every command in sections 3.1-3.2 except `/sc:load`" in the load row, P1 row, AC-1.1 and AC-1.2 (SPEC:112, SPEC:159, SPEC:195, SPEC:196). Per the Review Loop, guards on unchanged lines are not rebuilt here (round 1 covered them, `R1:28-71`). Three guards, six rows each, all cells populated (18 rows, 7 GAP). Every GAP is an FR-8 finding, mapped to a follow-up id in the Status column after the grading check.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| GA-1 P0 step 3 outcome matches the report's status | SPEC:194 | Zero/Empty | no report file exists | no status to match | `SPEC:63` maps "no report exists" to `failed`, and step 4 (`test -s`) then fails the phase | OK |
| GA-1 | SPEC:194 | One/Minimal | report says `status: succeeded`, worker sends `--outcome succeeded` | match | stated | OK |
| GA-1 | SPEC:194; SPEC:91 | Typical | troubleshoot, existing report `REPORT.md` (markdown) | the status the outcome must match is not shown to exist | the inventory lists `report_path` and `audit_log_path` for troubleshoot, no status (`INV-B:242`); whether `REPORT.md` carries one is UNVERIFIED, and the AFTER text says only "the status in the command's existing report" | GAP -> M-14 |
| GA-1 | SPEC:194; SPEC:63 | Maximum/Overflow | existing report holds a status outside `succeeded/partial/failed/blocked` (workflow's own contract vocabulary is not read, `REV1:36`) | undefined | `SPEC:63` maps only the four values; "matches" is not defined for others | GAP -> M-14 (carries round-1 M-7 onto a changed line) |
| GA-1 | SPEC:194; SPEC:83 | Sentinel Value Match | adversarial: contract exists but "filename not fixed" (two different locations seen, `INV-A:35`, `INV-A:60-61`) | "that file" is ambiguous | not stated which of `<output>/adversarial/return-contract.yaml` or `.../adversarial/adversarial/return-contract.yaml` is the report path | GAP -> M-14 |
| GA-1 | SPEC:194 | Legitimate Edge Case | the run ends `failed` or `blocked` and the worker reports `--outcome failed` | match | step 3 passes; "a failure here reopens section 1" names failures of the check, not of the command | OK (see N-9) |
| GA-2 P0 step 4 `test -s` on the existing report | SPEC:194 | Zero/Empty | 0-byte report file | `test -s` false | step 4 fails, phase fails | OK |
| GA-2 | SPEC:194 | One/Minimal | 1-byte report file | `test -s` true | step 4 passes; content is not parsed at P0 (stated: "step 4 is `test -s`") | OK |
| GA-2 | SPEC:194; SPEC:91 | Typical | `REPORT.md` with text | true | step 4 passes | OK |
| GA-2 | SPEC:194; SPEC:83 | Maximum/Overflow | two candidate report files (adversarial nested path) | one file tested | not stated which one step 4 tests | GAP -> M-14 |
| GA-2 | SPEC:194; SPEC:64 | Sentinel Value Match | a report file left by an earlier attempt at the same path, new run writes none | `test -s` true on a stale file | not stated that the file must be new in this run (the retry rule is round-1 M-8) | GAP -> M-14 |
| GA-2 | SPEC:194; SPEC:92 | Legitimate Edge Case | workflow stops before creating its package, so no contract exists ("Not written for pre-creation STOPs", `INV-B:272`) | `test -s` false | step 4 fails and the text reopens section 1; stated, though the defect is the P1 fix at SPEC:92; the smoke input is a "small change", which avoids it | OK |
| GA-3 membership "except `/sc:load`" | SPEC:112, SPEC:195 | Zero/Empty | a caller passes `--unattended` to `/sc:load` | load "takes no `--unattended`" | refuse or ignore is not stated | GAP -> M-15 |
| GA-3 | SPEC:195 | One/Minimal | the single excluded command, load | no section, no contract | AC-1.1 asserts load has none | OK |
| GA-3 | SPEC:159, SPEC:195 | Typical | another P1 command (for example analyze) | flag and section required | stated in the P1 row and AC-1.1 | OK |
| GA-3 | SPEC:195 | Maximum/Overflow | all other 36 commands of 3.1-3.2, plus the 6 section-4 commands | 36 have a section, the 6 and load have none | AC-1.1 asserts both sets | OK |
| GA-3 | SPEC:76, SPEC:112 | Sentinel Value Match | load is a "changed command" (usage line, P1) and SPEC:76 says "Every changed command also gains the `## Unattended mode` section" | the general sentence and the row disagree | the row states the exception and AC-1.1 enforces it; SPEC:76 does not say the row wins | GAP -> M-15 |
| GA-3 | SPEC:112, SPEC:138 | Legitimate Edge Case | a coordinator dispatches load as its own Task | contrary to the row | the row says "not as its own Task"; if it happens, `SPEC:63` ("no report exists") gives `--outcome failed` | OK |

Table complete. FR-10 gate satisfied: all cells populated, all three guards enumerated. 7 GAP rows generated 7 FR-8 findings; after the grading check all fall under the two Medium follow-up candidates M-14 and M-15 (each needs a reading choice or states a requirement the text never writes). None meets the blocking bar.

## Quantity Flow Diagram (pipeline dimensional analysis)

Triggered: the command set is filtered and fanned across phases, and the changed lines alter the count at three consumers. Counts below use the candidate's own numbers (`SPEC:76`, `SPEC:159`, `SPEC:195`).

```text
[43 commands in cmd/] --> [Stage 1: drop 6 coordinator-only (section 4)] --> [37 in 3.1 + 3.2]
   37 --> [Stage 2: P1 flag filter, "except /sc:load" (SPEC:159)] --> [36 commands accept --unattended]
   36 --> [Consumer AC-1.1, section asserted for 36 (SPEC:195)]            = 36  (conserved)
   37 - 36 = 1 (load) --> [Consumer AC-1.1, "neither /sc:load nor any section-4 command" has one] = 1 + 6 = 7  (conserved)
   P1-scheduled commands: 9 (incl. load) + 4 fixes = 13 --> [Stage 3: AC-1.2 filter, "except /sc:load"] --> [12 live checks (SPEC:196)]
        |
        v
   [Consumer: SPEC:76 "every changed command" = changed commands incl. load]  <-- load counted as changed, section count 36: stated by the row, MISMATCH IN WORDING ONLY (M-15)
```

Counts are conserved at every consumer the revision touched (36, 7 and 12). The round-1 divergence (37 flag and section holders against 13 commands with P1 work) is gone for load and remains for the 24 commands scheduled P2-P4 (round-1 M-2, unchanged lines, not re-graded). FR-19 would label the SPEC:76 wording mismatch CRITICAL only if a count changed outcome; here no count differs, so it stays a Medium wording note.

## === REQUIREMENTS ANALYSIS === (findings on changed lines)

No new blocking finding. Experts: Wiegers (lead), Adzic, Cockburn, with Whittaker.

### M-14 (MAJOR, graded Medium) origin=changed. AC-0.4's new pass condition leans on a report status and a report file that the text does not pin down.
- Expert: Adzic (lead), Wiegers. FR-8 for GA-1 rows 3, 4, 5 and GA-2 rows 4, 5. Priority Medium. Quality impact: Testability +1.
- Sentence: an implementer who follows AFTER `SPEC:194` checks that the `--outcome` "matches the status in the command's existing report" for troubleshoot, whose existing report is `REPORT.md` (`SPEC:91`) and whose inventory entry names no status field (`INV-B:242`), and for adversarial, whose contract path is "not fixed" (`SPEC:83`; `INV-A:60-61`), and must decide, with no stated rule, what the status of a markdown report is and which of two files is "that file".
- Why Medium: the operator can read a verdict out of `REPORT.md` and pick the contract the run wrote, so the gate can be passed; the wrong outcome needs an assumption (a stale file, an unmapped status). `REV1:36` already records the same limits as UNVERIFIED.
- Recommendation: add, in the same cell, one clause naming the status source for a markdown report (the report's stated result) and requiring the report file to be the one written by this run.

### M-15 (MAJOR, graded Medium) origin=changed for the flag question (SPEC:112); the SPEC:76 half is origin=unchanged and quotes the changed line it depends on. The load exception is stated in one row, not at the general rule.
- Expert: Wiegers (lead), Cockburn. FR-8 for GA-3 rows 1 and 5. Priority Medium. Quality impact: Consistency +1.
- Sentence: an implementer who follows `SPEC:76` ("Every changed command also gains the `## Unattended mode` section") adds that section to `/sc:load`, which is a changed command (usage line, `SPEC:159`), against AFTER `SPEC:112` ("gets no `## Unattended mode` section or contract"); and the load row never says what load does when a caller passes `--unattended` anyway.
- Why Medium: the row is the specific statement and AC-1.1 (`SPEC:195`) fails a load file that has the section, so the error is caught before it ships; load has no gate, so ignoring or refusing the flag changes nothing visible. `REV1:34` records that `SPEC:76` was left unedited on purpose, because no blocking finding named it.
- Recommendation: when next editing, add "except `/sc:load`" to `SPEC:76` and one clause on the flag (refuse or ignore).

## === ARCHITECTURE ANALYSIS ===

No finding in this bucket. Experts: Fowler (lead), Newman, Hohpe, Nygard. The revision keeps the central decision intact: P0 still edits no command (`SPEC:158`); P1 still gives every later phase a report file; load stays a step inside another worker's brief (`SPEC:112`, `SPEC:138`), which agrees with `INV-B:65` ("writes no file"); the shared 7.2 check keeps one definition and AC-0.4 states its P0 variant locally rather than forking 7.2. Interface check: the contract (WC-4) is still only required from P1 onward, and the P0 smoke runs use the report each command writes today, so no command is asked to write a file before its phase.

## Follow-up candidates (Medium and minor; none fails the review)

- M-14 and M-15 above.
- Round-1 follow-ups M-1 to M-13 and N-1 to N-7 (`R1:111-182`) concern unchanged lines and are not re-graded; the diff does not touch them, so none is closed or worsened, except that M-7 (outcome mapping holes) now also bears on AC-0.4 step 3 (carried into M-14).

### Minor notes (never fail the review)
- N-5 carried (origin=unchanged, quotes the changed line): AC-0.4 still omits `--unattended` from its three command lines (`SPEC:194`), while 2.3 requires it in every brief (`SPEC:73`). AFTER `SPEC:194` ("the contract arrives in P1") makes the omission consistent at P0, but 7.2 step 1 still says the brief follows 2.3 (`SPEC:180`). One clause would close it.
- N-9 (MINOR, origin=unchanged): AC-0.4 steps 3 and 4 pass for a command that ended `failed` or `blocked` if the worker reported it correctly (AFTER `SPEC:194`; 7.2 step 3 behaved the same in the baseline, `SPEC:182`). Phase 0 aims to show a direct command run completes and reports cleanly (`SPEC:272`); a happy-path requirement ("at least one command ends `succeeded`") would state it.
- N-10 (MINOR): reviser contract. The revision edited `SPEC:112`, which the round-1 reviser brief did not name (`R1:208` names AC-1.1, the P1 row and AC-1.2 for B-2); the edit is the one B-2's own recommendation offers ("say once that load accepts no `--unattended`", `R1:102`), carries its finding id, and adds no section or mechanism. I count it compliant. Each added span cites its finding id (`SPEC:112`, `SPEC:159`, `SPEC:194`, `SPEC:195`, `SPEC:196`), and the byte size is reported before and after (`REV1:9-13`), matching `wc -c` (57763 and 58099).

## expert_consensus
- Wiegers, Adzic and Cockburn: both blocking defects are fixed at the lines they named; the remaining weakness in the AFTER text is how precisely P0's report source is named (M-14).
- Fowler, Newman, Hohpe and Nygard: no architectural change was made and none is needed; the load carve-out follows the existing "step inside another brief" design.
- Whittaker: the changed guards break only under assumptions (a stale file, a status outside the four, a flag passed to a command that takes none); none yields a concrete wrong outcome from the AFTER text as written.
- Disagreement: none recorded.

## quality_assessment
Clarity 7, Completeness 6, Testability 6 (up from 5.5: the P0 gate can now pass), Consistency 6.5 (up from 6: load is now consistent in four of five places), overall 6.4 of 10.

## improvement_roadmap
- immediate: none required.
- short_term: M-14, M-15, then the round-1 short-term items (M-1, M-2, M-3, M-4, M-6, M-7, M-8, `R1:196`).
- long_term: round-1 long-term items and the minor notes.

## adversarial_analysis
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:194** (the outcome sent matches the status in the existing report) fails when **the existing report is troubleshoot's markdown `REPORT.md`, which names no status field in the inventory (`INV-B:242`)**. Concrete attack: before, step 3 asked for the contract's `status` and could never be met at P0 (B-1); after, step 3 asks for "the status in the command's existing report"; the worker reads `REPORT.md`, finds a diagnosis and a confidence but no status, sends `--outcome succeeded`, and the operator cannot say whether that "matches". Severity MAJOR, graded Medium (M-14).
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:194** (step 4 tests this run's report) fails when **the same output directory already holds a report from an earlier attempt**. Concrete attack: attempt 1 writes `REPORT.md`; attempt 2 dies before writing; `test -s` passes on attempt 1's file while the worker reports `failed`; step 3 compares against the stale status. Severity MAJOR, graded Medium (M-14; same family as round-1 M-8).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:112** (load takes no `--unattended`) fails when **a coordinator copies the section 2.3 brief template, which includes `--unattended` in every command line (SPEC:73), onto a load step**. Concrete attack: brief says `/sc:load --unattended`; the text does not say whether load refuses the flag or ignores it. Severity MINOR to MAJOR, graded Medium (M-15); no visible harm because load has no gate.
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:194** fails when **the report is 0 bytes**: `test -s` fails and the phase reports a failure, correctly. No finding.
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:195-196** (counts of commands tested) fails when **the exclusion is applied twice or not at all**: 37 minus 1 gives 36 sections and 12 live checks; the quantity diagram shows the counts conserved. No finding.

## Self-check (before the verdict)
Commands run in the sandbox against the diff output, with each quoted line stripped of its `<` or `>` prefix and matched as a whole line (`grep -nFx`):
- Every AFTER line (without `>`) is found in CANDIDATE at lines 112, 159, 194, 195, 196; none of the five is found in BASELINE (count 0).
- Every BEFORE line (without `<`) is found in BASELINE at lines 112, 159, 194, 195, 196; none of the five is found in CANDIDATE (count 0).
- No quote was missing, so no role was swapped. The decisions above were made from the AFTER text, and a PASS requires the AFTER text to be consistent with every requirement that depends on it: I checked `SPEC:63`, `SPEC:73`, `SPEC:76`, `SPEC:79`, `SPEC:81-92`, `SPEC:149`, `SPEC:154`, `SPEC:158`, `SPEC:182-183`, `SPEC:265` and `SPEC:272` against it. One wording tension remains (`SPEC:76` against `SPEC:112`, M-15), and the machine-checked requirement (`SPEC:195`) resolves it in favour of the row, so it is not a conflict an implementer would ship.

## Reviser brief
Blocking finding ids: none. Nothing needs revising for this review. If the user chooses to act on follow-up candidates M-14 and M-15 anyway, the rules from the Review Loop still hold (this restates them; the reviser reads this report, not the command): revise only text a finding names; add no rule, mechanism or section that no finding calls for; each added paragraph or table cites its finding id; report the byte size of the specification before and after the edit.

verdict: PASS
