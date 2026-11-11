review: 3 of 3

# Spec-panel re-review: orca-worker-contract-spec.md (round 3)

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md`
Candidate not edited. No other review started. Only this file was written.

## Roles and inputs (fixed)

| Role | File | sha256 |
|---|---|---|
| CANDIDATE (`@file`) | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (58510 bytes, 285 lines) | `bbc5da09c16d99c761039d7df263e9ff3629635be3ec1f834b924b06575af75f` |
| BASELINE (`--baseline`) | `.dev/orca-command-refactor/specs/history/spec-v2.md` (58349 bytes, 285 lines) | `49b44eed9e9476353afbf46c4ab057a94b41cde7cfd310c3fc03ba949d765180` |
| PRIOR (`--re-review`) | `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, `verdict: FAIL`, blocking B3) | `2c10bd7edf7fc2f94ecbe8a30b09c24a0018fc9a47e5554a67e6ab8306cba08d` |

The baseline hash equals the candidate hash round 2 recorded (`R2:12`), so the baseline is the text round 2 reviewed. All three inputs are readable and non-empty. PRIOR's header is `review: 2 of 3` (`R2:1`), so N = 2 + 1 = 3. The cap check (a prior at `review: 3` with FAIL means do not review) does not fire: PRIOR is at 2.

Citation keys: `S:N` = line N of the candidate; `B:N` = line N of the baseline; `R2:N` = line N of PRIOR; `R1:N` = line N of `review/round1.md`; `REV2:N` = line N of `review/revise2.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `CMD:N` = line N of `command.md`. This round needed no inventory line: the changed text cites none. Every citation to a file outside the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, `cmd/` and `sk/` lines not echoed in an inventory) is UNVERIFIED.

## Step 1. Evidence block (`diff -w BASELINE CANDIDATE`)

Command run: `diff -w specs/history/spec-v2.md specs/orca-worker-contract-spec.md`. Not empty: 2 changed lines (hunks `76c76` and `195c195`; no line added or removed). A plain `diff` without `-w` reports the same two hunks, so no whitespace-only change exists. Lines copied verbatim.

### BEFORE (baseline)

~~~~text
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<contract-dir>/return-contract.yaml`. Every changed command except `load` (no contract, row below) also gains the `## Unattended mode` section (section 2.1), in the phase its row names. Phase numbers refer to section 6.
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` and the P4 commands (implement, post-release, pr-submit, which get theirs in P4 after D2-D4) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that `load` and no section-4 command has one | passes |
~~~~

### AFTER (candidate)

~~~~text
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<contract-dir>/return-contract.yaml`. Every changed command except `load` (no contract, row below) also gains the `## Unattended mode` section (section 2.1), in the phase its row names; brainstorm and init-lite, whose rows name none, gain it in P1. Phase numbers refer to section 6.
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command whose section is due in P1 under section 3 (the rows naming P1, plus brainstorm and init-lite) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`; the sections due in P2, P3 and P4 (the last after D2-D4) are asserted in the check of the phase their row names; and the test asserts that `load` and no section-4 command has one | passes |
~~~~

Line map (same in both files): `76` = section 3 preamble; `195` = AC-1.1 row. The only new words in S:76 are "; brainstorm and init-lite, whose rows name none, gain it in P1". S:195 is rewritten from a P1 test over "every command ... except `load` and the P4 commands" into a phase-scoped test. Nothing else changed: S:62 (WC-4), S:83, S:92, S:154, S:159 and every row are as round 2 reviewed them.

## What was covered

- Read in full: the candidate (285 lines), PRIOR, `review/revise2.md`, README, `command.md`; read the tail of `review/round1.md` (R1:225-253) for the carried follow-ups. The inventories were not needed (the changed text cites none).
- Experts run, fixed order: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (active in every panel review). Crispin, Gregory and Hightower are outside the two focus areas and were not run.
- Scope: the two changed lines, the prior blocking finding B3 and the two earlier resolved findings B1 and B2 (re-checked for regression), and the text that depends on the changed lines (S:62, S:79, S:84, S:87, S:99-125, S:112, S:154, S:159-162, S:196, S:208-210, S:240, S:265). Inherited text is cited only through the changed line it depends on (Review Loop bullet 5).
- `rf-qa.md` (Review Loop bullet 5, steps 1-5 of its Fix Cycle process): not present in the sandbox (`ws/.claude/` does not exist; `home/.claude/` holds only an empty `rules/` directory), so it is unread. The rules in Review Loop bullet 5 were applied alone, as the command allows.
- Grading rule: command bullet 2 makes FR-8/FR-9 findings blocking. As in rounds 1 and 2, the brief ("Report concrete wrong outcomes ... list Medium and minor findings under follow-up candidates") narrows that: a table GAP becomes blocking only if it names a concrete wrong outcome that needs no further assumption; otherwise Medium. Bullet 7 lets a brief narrow and not widen; the coordinator should know this choice was made. It decides nothing this round: the single GAP row (G1 row 6) is the same defect as M18 and it needs an assumption (see M18).
- Not covered: the commands' own behaviour (files outside the workspace), Orca internals, any live run, M1 to M17 (not touched by the diff, not re-graded), and the wording of rows other than the ones cited.

## Table 1. Prior blocking findings

| Id | Prior defect | AFTER text compared | Status |
|---|---|---|---|
| B1 | AC-1.1 required a `## Unattended mode` section on `load`, which the load row and Decisions say has no contract, and on implement, post-release and pr-submit before D2-D4 (R1:98-103; resolved in R2:59). | S:195 AFTER ends "and the test asserts that `load` and no section-4 command has one"; S:76 AFTER still says "Every changed command except `load` (no contract, row below)". Load row S:112 ("none (see note)") and Decisions S:265 are untouched and agree. The three P4 commands are no longer asserted at P1: S:195 AFTER puts "the sections due in ... P4 (the last after D2-D4)" in "the check of the phase their row names". | **resolved**, not regressed. |
| B2 | WC-4 contract location contradicted by tdd and init-lite (file-valued `--output`), adversarial, workflow and spec-panel (R1:139-143; resolved in R2:60). | S:62 (WC-4), S:83 and S:92 are not in the diff; `<contract-dir>` is defined as in round 2, and S:76 AFTER keeps "Contract means the WC-4 file `<contract-dir>/return-contract.yaml`". | **resolved**, not regressed. |
| B3 | S:76 puts each `## Unattended mode` section "in the phase its row names" while AC-1.1 asserted all of them at P1: 33 asserted vs 12 due at the P1 check (R2:116-122), so P1 could not pass and S:154 held P2 closed; brainstorm and init-lite were in AC-1.1's set but in no phase. | S:195 AFTER asserts at P1 only "every command whose section is due in P1 under section 3 (the rows naming P1, plus brainstorm and init-lite)" and defers P2, P3 and P4 sections to "the check of the phase their row names". S:76 AFTER adds "brainstorm and init-lite, whose rows name none, gain it in P1". The two lines now use one rule. Count against the rows (S:83-92, S:99-125): P1 due = 8 phase-P1 rows of 3.2 (analyze, build, business-panel, design, document, explain, index, test) + 4 P1 fixes of 3.1 (adversarial, cleanup-audit, index-repo, workflow) + brainstorm + init-lite = 14; S:195 asserts those 14 and S:76 makes those 14 due. S:154 ("Later phases do not start until the earlier phase's checks ... pass") no longer blocks P2 by contradiction. | **resolved**. Residuals are Medium (M19, M20). |

## Guard Condition Boundary Table (hard gate FR-10: complete before synthesis)

Re-review scope: guards on changed lines only (Review Loop bullet 5). Guards: G1 `p1_due_set` (S:195), G2 `section_phase` (S:76), G3 `load_exclusion` (S:76, S:195). 3 guards x 6 rows, all cells populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `p1_due_set` | S:195 | Zero/Empty | a command whose row names no phase | would fall out of the set | brainstorm and init-lite are the only ones ("Small fix" = None, S:84, S:87; every other 3.1 row names a phase, S:83, S:85, S:86, S:88-92); S:195 adds them to the P1 set by name | OK |
| G1 | S:195, S:112 | One/Minimal | load, whose Phase cell is "P1 (usage line only)" | matches "the rows naming P1" read literally | Excluded by "whose section is due in P1 under section 3" (S:76: load has none) and by the closing clause "`load` ... has none"; a literal reader meets both and resolves it at once (N13) | OK |
| G1 | S:195, S:99 | Typical | analyze (row phase P1) | section asserted in the P1 check | Asserted at P1; its section lands in P1 (S:76) | OK |
| G1 | S:195, S:100 | Maximum/Overflow | auggie-review and the other 14 P2 commands, the 4 P3 commands (counts from S:88-91, S:99-125) | section due after P1 | Not asserted at P1; asserted "in the check of the phase their row names" (S:195). S:154 no longer blocks P2 | OK |
| G1 | S:195, S:84, S:87 | Sentinel Value Match | the value "None" in the 3.1 "Small fix (phase)" column | read as "no phase" | S:76 AFTER reads it as "rows name none ... gain it in P1"; the two commands have a section but no small fix, so nothing else is read as a phase | OK |
| G1 | S:195, S:240 | Legitimate Edge Case | pr-submit under recommended D3(a) ("no pr-submit changes in Phase 4") | section "due in P4 (the last after D2-D4)" | S:195 says the section is asserted in the P4 check; AC-4.1 to AC-4.3 (S:208-210) assert no section, and D3(a) gives pr-submit no change; which of the two wins is not stated | GAP (M18) |
| G2 `section_phase` | S:76, S:84, S:87 | Zero/Empty | row naming no phase | no phase to land in | Explicit clause: P1 | OK |
| G2 | S:76, S:83 | One/Minimal | one-phase 3.1 row (adversarial, P1) | section in P1 | Section in P1; the 3.1 header says the named file is reported "until Phase 1 adds the contract" (S:79) | OK |
| G2 | S:76, S:99, S:195 | Typical | analyze at the P1 check | has section | Section lands in P1, asserted in P1 | OK |
| G2 | S:76, S:88, S:195 | Maximum/Overflow | reflect (3.1, small fix P2) at the P1 check | section due in P2 | Not asserted at P1 (S:195); due in P2 (S:76); S:154 consistent | OK |
| G2 | S:76, S:112 | Sentinel Value Match | the phase text "P1 (usage line only)" on load | names P1 | S:76 excludes load; S:195 asserts load has none | OK |
| G2 | S:76, S:113 | Legitimate Edge Case | P4 rows (implement, post-release, pr-submit) | phase P4 | Section "in the phase its row names" = P4, after D2-D4; same as the P4 case of G1 | OK |
| G3 `load_exclusion` | S:76, S:195 | Zero/Empty | load has zero sections | none | Asserted as none (S:195) and stated as none (S:76, S:112, S:265) | OK |
| G3 | S:195, S:159 | One/Minimal | `--unattended` on load | flag accepted | S:159: accepted "(a no-op where a command has no gate)"; no section needed | OK |
| G3 | S:195, S:128 | Typical | a section-4 command (agent, git, help, pm, spawn, swarm-wizard) | no section | Asserted none (S:195), and section 4 says no `--unattended` mode (S:128) | OK |
| G3 | S:195 | Maximum/Overflow | a command in both load's and a P-phase's set | cannot occur | Load is one row; no command is in two phases | OK |
| G3 | S:76, S:195 | Sentinel Value Match | "except `load`" in S:76 vs "`load` ... has none" in S:195 | same exclusion | Both exclude exactly load | OK |
| G3 | S:195, S:128 | Legitimate Edge Case | a 3.2 command that becomes coordinator-only (pr-submit under D3(a)) | in no set | Same as G1 row 6 (M18) | OK (carried to M18) |

GAP rows: 1 (G1 row 6). It is the same defect as M18 and is graded Medium (see M18). Table is complete; synthesis proceeds.

## Quantity Flow Diagram (FR-21)

Pipeline Dimensional Analysis applies: the commands pass through a 3-way split and a 5-phase rollout, and AC-1.1 is a consumer of those counts.

```text
[cmd/ commands: 43 (S:76)] --> [Classify] --> [3.1 ready: 10][3.2 change: 27][S4 coordinator-only: 6]   10+27+6 = 43
        |
        v
[Sections by the phase that makes them due (S:76 AFTER)]
        |-- P1: 8 (3.2 rows) + 4 (3.1 P1 fixes) + 2 (brainstorm, init-lite) = 14
        |-- P2: 11 (3.2) + 4 (3.1: reflect, release-split, tdd, troubleshoot) = 15
        |-- P3: roadmap, save, validate-roadmap, validate-tests = 4
        |-- P4: implement, post-release, pr-submit = 3 (after D2-D4)
        |-- none: load = 1
        |-- 14 + 15 + 4 + 3 + 1 = 37 = 10 + 27
        v
[Consumer AC-1.1 at P1 (S:195 AFTER): expects 14; producer yields 14]            <-- NO MISMATCH (B3 was 33 vs 12)
[AC-1.1 defers 15 + 4 + 3 = 22 sections to later checks; AC-2.1, AC-3.1, AC-4.1 to AC-4.3 do not name the assertion]   <-- UNCHECKED CONSUMER (M20, M18)
[S:154: P2 starts when the P1 checks pass]  --> P1 can pass, P2 can start
```

Severity per FR-19: no CRITICAL mismatch. The only count gap is the unchecked consumer line (22 sections have a stated assertion point that no later check line names), graded Medium (M20), because the sentence in S:195 states the requirement and a count of 14 at P1 is met.

=== REQUIREMENTS ANALYSIS ===
Experts: Wiegers (lead), Adzic, Cockburn.

No new blocking finding. B3 is fixed: S:76 AFTER and S:195 AFTER agree on the P1 set (14) and on where the rest lands (Table 1, Quantity Flow Diagram). Wiegers: the acceptance statement is now traceable to the rows it tests, row by row. Adzic: the example "P1 = analyze ... plus brainstorm and init-lite" can be run as written; the load edge case is stated twice. Cockburn: the actors are the same as before (implementer, coordinator, test author).

=== ARCHITECTURE ANALYSIS ===
Experts: Fowler (lead), Nygard, Newman, Hohpe.

No new blocking finding. The phase-scoped assertion is the less invasive of the two fixes round 2 offered (R2:122): it leaves S:154 and every row as they were. Nygard: failure mode of the fix, a later phase whose section assertion is never written, is the M20 residual. Whittaker (Sequence Attack): run P1 to completion as S:76 prescribes; `uv run pytest tests/skills/test_worker_contract.py -q` asserts 14 sections, all written in P1, so it passes and S:154 lets P2 start (round 2 had 19 failures here, R2:121). Whittaker (Accumulation Attack): the counts add up (14 + 15 + 4 + 3 + 1 = 37; 37 + 6 = 43). Whittaker (Divergence Attack): load is the one command whose Phase cell names P1 yet whose section is not due; the closing clause of S:195 settles it (N13).

## Follow-up candidates (Medium, not blocking)

- **M19 (origin=unchanged, depends on changed S:76). The 3.1 header still says brainstorm and init-lite have no change.** S:79 (unchanged) says "The only command changes are the small fixes in the last column", and the brainstorm and init-lite rows say "None" (S:84, S:87). The changed S:76 says those two "gain it [the section] in P1", and S:195 asserts it. The same loose wording applies to the other eight 3.1 commands, which also gain a section on top of their small fix. Wrong outcome: an implementer who builds P1 from the 3.1 rows alone leaves the two commands unchanged and the P1 test fails on them, a delay caught by AC-1.1 itself. Medium. Fix: change "The only command changes are the small fixes" to also name the section. S:159's command list (unchanged) also omits the two commands; its sentence "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" still covers them.
- **M20 (origin=changed). P2, P3 and P4 section assertions have no check line.** S:195 AFTER says those sections "are asserted in the check of the phase their row names". AC-2.1 asserts one assertion "per gate listed in the section 3 row" (S:199), AC-3.1 asserts report filenames and flags (S:204), AC-4.1 to AC-4.3 assert behaviour (S:208-210); none says the test also asserts the section exists. The reviser noted the same (REV2:30). Wrong outcome: a P2 plan built from the P2 block alone checks gates and not section presence, so a P2 command without its section can pass, until a reader goes back to the P1 row. The requirement is stated in S:195, so Medium. Fix: one clause in each of AC-2.1 and AC-3.1 ("and the section of every command whose row names this phase").
- **M18 (origin=changed, carried from R2:135). Nothing asserts the P4 sections, and D3(a) gives pr-submit none.** S:195 AFTER keeps "P4 (the last after D2-D4)"; AC-4.1 to AC-4.3 (S:208-210) assert no section; D3(a), the recommended answer, says "no pr-submit changes in Phase 4" (S:240) and S:139 keeps pr-submit a worker candidate only if D3 is accepted. Wrong outcome needs two assumptions (the user answers D3(a), and an implementer applies S:195 to pr-submit blindly), and the decision comes before P4 starts, so Medium. This is the G1 GAP row.
- M1 to M17 of rounds 1 and 2 (R1:237, R2:131-135) remain as listed there; the diff did not touch their text. M4 (flag accepted in P1 before its gate row lands, S:159) is the one nearest the changed lines: unchanged and still Medium.

Minor notes (never fail the review):
- N13 S:195 AFTER says "the rows naming P1" and the load row's Phase cell is "P1 (usage line only)" (S:112). Read literally, load is in the P1 set and also asserted to have none. The qualifier "whose section is due in P1 under section 3" and the closing clause settle it. Suggest "the rows naming P1 other than load".
- N14 AC-1.2 (S:196, unchanged) runs the 7.2 live check on "each P1 command" with `--unattended --output <dir>`. That set already contained load (no contract, so 7.2 step 4 cannot pass; S:265 says load is not its own Task), cleanup-audit and index-repo (no `--output` flag) and workflow (`--output-dir`), and now S:76 adds init-lite (file-valued `--output`, S:87). The text was not changed and round 1 did not grade it. It is not a new defect and, as it needs the reader to run the check on a command the spec says is not a Task, no wrong outcome is named. Origin: older than round 1.
- N15 REV2:9 reconciles with the files: baseline 58349 bytes and candidate 58510 bytes (net +161) match `wc -c` run here, and the two edited lines (76, 195) match the two diff hunks, so the reviser touched nothing else.
- N16 UNVERIFIED here (outside the workspace): every `cmd/` and `sk/` line the rows cite, `pyproject.toml:38` (S:183) and the claim in S:285 that 340 citations were checked. The changed lines cite none.

## Quality assessment and consensus

```yaml
specification_review:
  original_spec: ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
  sha256: "bbc5da09c16d99c761039d7df263e9ff3629635be3ec1f834b924b06575af75f"
  baseline_sha256: "49b44eed9e9476353afbf46c4ab057a94b41cde7cfd310c3fc03ba949d765180"
  review_date: "2026-11-10"
  review: "3 of 3"
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Newman, Hohpe, Whittaker]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.8
  clarity: 8
  completeness: 7
  testability: 7
  consistency: 8
critical_issues: []
expert_consensus:
  - "B3 is fixed: the section schedule (S:76) and its acceptance test (S:195) now use one rule and the counts reconcile (14 + 15 + 4 + 3 + 1 = 37) (Wiegers, Fowler)."
  - "B1 and B2 stay resolved; the edit touched neither S:62 nor S:112 (Cockburn, Newman)."
  - "The remaining work is wording: name the section in the P2 and P3 checks and in the 3.1 header (Adzic, Hohpe)."
improvement_roadmap:
  immediate: []
  short_term: [M19, M20]
  long_term: [M18, M14, M16, M15, M17]
adversarial_analysis: "see Sequence, Accumulation and Divergence attacks under ARCHITECTURE ANALYSIS and Table G1/G2/G3"
```

## Outcome of the review cap

This is review 3 of 3. No blocking finding is open, so no escalation is needed, and no Reviser brief is written (it is omitted at `review: 3`). Had a blocking finding been open, the run would escalate to the user with it.

## Self-check before the verdict

Run with `grep -nxFf` (whole-line match), stricter than `-nF`; the AFTER lines were taken from `diff -w` without the `>` and the BEFORE lines without the `<`.
- Each AFTER line found in CANDIDATE: lines 76 and 195, both found; 0 of 2 found in BASELINE.
- Each BEFORE line found in BASELINE: lines 76 and 195, both found; 0 of 2 found in CANDIDATE.
- Roles confirmed, no swap. `diff -w` and plain `diff` both report only hunks 76c76 and 195c195.
- The AFTER text is consistent with the requirements that depend on it: S:154 (P2 starts when the P1 checks pass; the P1 set is 14 and all 14 are due in P1), S:112 and S:265 (load has none, asserted in S:195), S:62 (unchanged), S:159 (the flag reaches every 3.1 and 3.2 command; wording only, M19), S:160-162 (the phase scopes name the same P2 to P4 commands the rows name). The residuals are wording gaps with no wrong outcome that needs no further assumption (M18, M19, M20).

verdict: PASS
