# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (`variant-1-original.md`, reviewer 1, analyzer), combined score 0.929 (`base-selection.md`, "Combined Scoring")
- Incorporating strengths from: Variant C (`variant-3-original.md`), Variant B (`variant-2-original.md`), and the Round 2.5 invariant probe (`invariant-probe.md`, no variant)
- Output: ONE merged verdict card at `R/adversarial/merged-verdict.yaml`, where R = `.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307`
- Planned changes: 10
- Merged findings: 19 (15 adjudicated by the advocates, 4 entered from the probe and marked not adjudicated)
- Merged verdict: **FAIL**; blocking count **2** (1 adjudicated: R3-F1; 1 not adjudicated: INV-001)
- Convergence: 1.00, status BLOCKED_BY_INVARIANTS (`debate-transcript.md`, "Convergence Assessment")
- Risk level: Medium overall (the base's verdict is replaced, and four unadjudicated items are added)

Citation keys are the ones defined in `debate-transcript.md` ("Citation Key"): `VA/VB/VC:N` cards, `DA:N` diff analysis, `R1a..R2c:N` rounds, `INV:N` probe, `TL:N` plan, `SRC:N` spec, `qa.md:N` executor QA rules, `SK:N` adversarial SKILL.md. `DT` is `debate-transcript.md` and `BS` is `base-selection.md`. Every cited line was opened for this step.

Calibrated reviewer confidences used below come from each card's calibration block: R1 (Variant A) 0.86 (VA:123), R2 (Variant B) 0.82 (VB:91), R3 (Variant C) 0.88 (VC:219). Every card's calibrator marked every one of its severities as holding (VA:124, VB:92, VC:220).

## Planned Changes
### Change 1: Replace the verdict and add R3-F1 as the adjudicated blocker (from Variant C)
- **Source**: Variant C, `verdict` and finding R3-F1 (VC:4, VC:7-28)
- **Target**: merged card `verdict` (replace PASS with FAIL) and `findings` M-01 (insert first)
- **Rationale**: DT X-001 95% and X-002 90%, unanimous; A and B conceded (R1a:36-44, R1b:35-37). Recorded as "can halt", not "will halt" (R2a:36, R2b:81, R2c:9).
- **Integration point**: drop the base's "I found no blocking defect" (VA:112) from the rationale; state the two gates (qa.md:52 and qa.md:61 for Task 4 QA; qa.md:310 and qa.md:286 for the managed FINAL)
- **Risk**: Medium. It reverses the base's verdict.

### Change 2: Merge the Task 6 phase-slot findings (from Variant C, into base R1-F3)
- **Source**: Variant C R3-F5 (VC:91-110); base R1-F3 (VA:47-66)
- **Target**: `findings` M-03 (restructure)
- **Rationale**: DT C-001 65%, decided 2-1 for should-fix (A at 0.60, R2a:97; C at 0.60, R2c:102). **Dissent: Variant B grades it blocking at 0.60** (R2b:108) and accepts should-fix as a fallback (R2b:64). Record the dissent in the finding.
- **Integration point**: keep A's D3 (a) grounding (SRC:61, SRC:201, SRC:224); add C's keying rule and B's five categories (R2b:66-71, R2c:64); drop the false agent-hit and `git merge-base` examples (R2b:40, R2c:19)
- **Risk**: Medium. The merged fix rewrites a task instruction, and INV-010 (M-18) must ship with it (INV:22).

### Change 3: Merge the quoted-phrase findings (from Variant C, into base R1-F1)
- **Source**: Variant C R3-F3 (VC:48-70); base R1-F1 (VA:7-25)
- **Target**: `findings` M-05 (restructure)
- **Rationale**: DT C-003 92%, unanimous; C conceded A's instance leads and withdrew "only way out" (R1c:43, R2c:13)
- **Integration point**: class drift for the instance (TL:112 against SRC:122); the general mechanism is noted as class none (R2a:50)
- **Risk**: Low. INV-014 (M-19) limits how the fix is worded.

### Change 4: Merge the Task 3 evidence findings and correct a base claim (from Variant B)
- **Source**: Variant B R2-3 (VB:42-57); base R1-F5 (VA:86-104)
- **Target**: `findings` M-09 (replace R1-F5's evidence text)
- **Rationale**: DT C-002 92% and X-004 85%; B conceded (R2b:15)
- **Integration point**: replace "two tests" (VA:95) with "one test reads the plugin core copy" and the `:308` citation (VA:100) with `:309` (R1a:47, VA:130); add SRC:252 and the existing plugin core files (R1c:59)
- **Risk**: Low

### Change 5: Add Variant C's should-fix findings R3-F2, R3-F4 and R3-F6
- **Source**: VC:29-47, VC:71-90, VC:111-127
- **Target**: `findings` M-04, M-07, M-08 (append)
- **Rationale**: DT X-003 80%; U-008 and C-005 unanimous (R2a:73-74, R2b:87-88, R2c:78-79)
- **Integration point**: in M-08 replace the line-290 citation with lines 341, 819 and 1091 (R2c:15)
- **Risk**: Low. Additive.

### Change 6: Add Variant C's minor findings R3-F7, R3-F8, R3-F9 and R3-F11
- **Source**: VC:128-169, VC:185-200
- **Target**: `findings` M-12 to M-15 (append)
- **Rationale**: unanimous minor (R2a:78-81, R2b:92, R2c:83-86); R3-F11 also fills the gap A recorded but did not file (VA:117-118, R1a:46)
- **Integration point**: append after the should-fix block
- **Risk**: Low

### Change 7: Add Variant B's R2-1 and merge R2-2 with C's R3-F10
- **Source**: VB:7-41; VC:170-184
- **Target**: `findings` M-10 and M-11 (append)
- **Rationale**: R2-1 downgraded to minor by all three (R2a:76, R2b:17, R2c:23); R2-2 and R3-F10 merged as minor (R2a:77, R2b:25, R2c:82)
- **Integration point**: R2-1 keeps class drift (R2b:17)
- **Risk**: Low

### Change 8: Enter the probe's real plan defects as not-adjudicated findings
- **Source**: `invariant-probe.md` INV-001, INV-002, INV-010, INV-014 (INV:5, 6, 14, 18)
- **Target**: `findings` M-16 to M-19 with `adjudicated: false`, and `unaddressed_invariants`
- **Rationale**: the gate blocks on INV-001 (DT "Invariant-Probe Gate"; SK:1461-1464); the probe states the debate's sufficiency claim is false as written (INV:27)
- **Integration point**: severity maps HIGH to blocking and MEDIUM to should-fix; each finding says the advocates did not debate it
- **Risk**: Medium. These findings carry no adversarial check.

### Change 9: Add run conditions and notes
- **Source**: INV-005 and INV-007 (INV:9, INV:11); B's matrix_omissions (VB:58-64); B's empty hunk H4 (VB:47-50); A's Task 7 check (VA:110-112)
- **Target**: `run_conditions` (new) and finding-free notes inside `provenance`
- **Rationale**: INV-005 and INV-007 depend on how the plan is run, not on its text; the notes were kept as notes by all three advocates (R2a:82-83, R2b:93-94, R2c:87-88)
- **Integration point**: `run_conditions` list; `provenance.notes`
- **Risk**: Low

### Change 10: Fill the merge metadata
- **Source**: DT, BS, this plan
- **Target**: `merge_method`, `base_variant`, `convergence_score`, `convergence_status`, `blocking_count`, `rejected_changes`, `provenance`
- **Rationale**: required top-level keys (section (d))
- **Integration point**: top of the YAML
- **Risk**: Low

## (a) Merged Finding List
Deduplicated by the diff-analysis topics (C-NNN, X-NNN, U-NNN; DA:41-104). Severity is the debate outcome (DT "Scoring Matrix" and its U-NNN supplement). "Reviewers" lists each card that raised the item, with that card's calibrated confidence.

| ID | Topic | Card items | Final severity | Class | Reviewers (calibrated) | Debate outcome | Citations to keep | One-line fix |
|---|---|---|---|---|---|---|---|---|
| M-01 | X-002, U-006 | R3-F1 | **blocking** ("can halt") | drift | R3 0.88 | unanimous, 90% (R2a:96, R2b:107, R2c:101) | TL:21, TL:24, TL:90, TL:93, SRC:220, qa.md:52, qa.md:61, qa.md:310, qa.md:286 | Reword TL:21: "P0 edits no command file, no SKILL.md and no agent file; the only file written under a skills directory is the byte-for-byte copy of HOW-WE-WORK.md in plugins/superclaude/skills/sc-recommend/refs/ that Task 4 makes" (VC:26-28). |
| M-02 | U-001 | R1-F4 | should-fix (fix first) | none | R1 0.86 | unanimous (R2a:68, R2b:82, R2c:73) | TL:17-27, TL:22, TL:37, SRC:59 | Add a Constraints line: the contract and the HOW-WE-WORK.md section use installed `~/.claude/...` paths only and copy no CAPS:/INV- ids or `src/superclaude/` paths (VA:84-85). |
| M-03 | C-001 | R1-F3 + R3-F5 | should-fix, **decided 2-1; dissent: B (blocking, 0.60)** | drift | R1 0.86, R3 0.88 | majority, 65% (R2a:97, R2c:102; dissent R2b:108) | TL:125, SRC:61, SRC:201, SRC:224, SRC:305 | Replace TL:125's two-way rule with five categories (WC-9 allowed; refused or deferred in a named phase; never a worker; no command converts this file; read-only or false match), key entries by path, verb and stripped line text, and scan with word boundaries (R2b:66-71, R2c:64). |
| M-04 | X-003, U-007 | R3-F2 | should-fix | drift | R3 0.88 | unanimous, 80% (R2a:98, R2b:110, R2c:104) | TL:22, TL:58, SRC:59, SRC:84, SRC:220 | Add to TL:22: "plus, in the brief template only, the section 3.1 'Brief must pass' flags and the section 6 phase markers (`--report-dir` from P1)" (VC:46-47). |
| M-05 | C-003 | R1-F1 + R3-F3 | should-fix | drift (the instance; the general mechanism is none) | R1 0.86, R3 0.88 | unanimous, 92% (R2a:71, R2b:85, R2c:76) | TL:56, TL:104, TL:112, SRC:122 | In TL:56 and TL:112 use the spec's "maximum of 10 inputs" / "never exceeds 10" and drop "(as written in section 2.3)"; have Tasks 1-2 record the phrase each rule will be tested on (VC:67-68), worded as M-19 requires. |
| M-06 | U-002 | R1-F2 | should-fix | none | R1 0.86 | unanimous (R2a:72, R2b:86, R2c:77) | TL:47, TL:72, TL:93-94, TL:147-152, TL:157, qa.md:85 | In Task 8, re-run AC-0.1, AC-0.2, AC-0.3, AC-C1 and AC-C2 and save each output to `./artifacts/<id>.txt` as the report's evidence (VA:45-46). |
| M-07 | U-008 | R3-F4 | should-fix (applies only if Task 3 adds the copy) | none | R3 0.88 | unanimous (R2a:73, R2b:87, R2c:78) | TL:69, TL:74, qa.md:310 | If Task 3 adds the plugin core copy, Task 5's test asserts it is byte-identical to the src file, like `test_plugin_mirror_matches_src` (VC:88-90). |
| M-08 | C-005 | R3-F6 (A noted it, VA:110-111) | should-fix | none | R3 0.88 | unanimous, 90% (R2a:74, R2b:88, R2c:79) | TL:90, TL:93; routing test lines 341, 819, 1091 (R2c:15) | Add to Task 4: the new section is ASCII only and is a new top-level section after the last one, outside the level-table and routing markers (VC:126-127). |
| M-09 | C-002, X-004 | R1-F5 + R2-3 | minor | none | R1 0.86, R2 0.82 | unanimous, 92% (R2a:75, R2b:89, R2c:80) | TL:69, SRC:252; `scripts/build_superclaude_plugin.py:75`, `tests/commands/test_routing_plugin_parity.py:3`, `tests/commands/test_impact_command.py:309` (VA:98-100, VA:130) | In Task 3, name build-script line 75 (no `core` in the copied folders), the parity test, the one test that reads a plugin core copy, and SRC:252's by-name exclusion. |
| M-10 | U-003 | R2-1 | minor | drift | R2 0.82 | unanimous (R2a:76, R2b:90, R2c:81) | TL:19, SRC:304-306 | Delete the AC-0.8 sentence, or replace it with "the P1 checks are AC-1.1 to AC-1.8 (section 7.3)" (VB:23). |
| M-11 | U-004 + U-012 | R2-2 + R3-F10 | minor | none | R2 0.82, R3 0.88 | unanimous (R2a:77, R2b:91, R2c:82) | TL:19, TL:154, SRC:238, SRC:303-304 | End the static report with a "results the P0 live plan must cite" list (VB:41), and add the coordinator's re-staging of `.dev/tasks` and AC-C4 re-run to the next steps (VC:183-184). |
| M-12 | U-009 | R3-F7 | minor | none | R3 0.88 | unanimous (R2a:78, R2b:92, R2c:83) | TL:115, SRC:306 | Write the negative check as a cumulative per-phase map, `{"P0": set()}` (VC:140-141). |
| M-13 | U-010 | R3-F8 | minor | none | R3 0.88 | unanimous (R2a:79, R2b:92, R2c:84) | TL:58 | In Task 5, assert each template flag exists in its command file, except the "from P1" flags (VC:154-155). |
| M-14 | U-011 | R3-F9 | minor | none | R3 0.88 | unanimous (R2a:80, R2b:92, R2c:85) | TL:15, TL:90 | Reword the Goal: the Orca section is in HOW-WE-WORK.md and its plugin copy; the CLAUDE.md level-table copy is unchanged (VC:168-169). |
| M-15 | C-004 | R3-F11 (A noted it, VA:117-118) | minor | none | R3 0.88 | unanimous, 92% (R2a:81, R2b:92, R2c:86) | TL:33-35, TL:96 | In Task 1 also save `make verify-sync` output, and add `tests/docs` and `tests/unit` to the wider baseline and Task 4's comparison (VC:199-200). |

Severity totals for the adjudicated findings: 1 blocking, 7 should-fix, 7 minor. Section (b) adds 1 blocking and 3 should-fix that were not adjudicated.

## (b) Round 2.5 Invariants in the Merged Verdict
None of these items was seen or debated by an advocate; the probe ran after Round 2 (INV:1-2). Each one enters the merged card as a finding with `adjudicated: false` and `source: invariant-probe`, and also as a row of `unaddressed_invariants`. Severity mapping: HIGH becomes blocking, MEDIUM becomes should-fix (the gate blocks on HIGH and only warns on MEDIUM, SK:1461-1466).

| ID | Invariant | Final severity | Class | Adjudicated | Citations to keep | One-line fix |
|---|---|---|---|---|---|---|
| M-16 | INV-001 (HIGH, sufficiency_challenge): the Task 1 wider baseline already fails (8 failed), Task 1 must save it as evidence, and the managed FINAL returns `issues` when a cited log "shows a failure at its outcome line" | **blocking** | none | **no** | TL:35, TL:48, TL:95, qa.md:310, qa.md:294, qa.md:286 (INV:5) | In TL:35 and TL:95 say pre-existing failures are expected, list the 8 failing test ids as the accepted baseline, and cite the per-test comparison file, not the raw log, as evidence (INV:5). |
| M-17 | INV-002 (MEDIUM, state_variables): the wider suite rewrites the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json`, which then enters Tasks 1 and 4's diffs | should-fix | none | **no** | TL:35, TL:95, TL:154, qa.md:51 (INV:6) | Add `--deselect tests/cli/eval/test_perf_home_setup.py` to the wider runs, or `git restore` that path after each run, in TL:35 and TL:95 (INV:6). |
| M-18 | INV-010 (MEDIUM, interaction_effects): TL:125 counts `-f`/`-F` as a `gh api` post, so six `--method GET` reads are "posts" under the plan and "reads" under M-03's fix | should-fix | drift | **no** | TL:125, SRC:305, qa.md:50, qa.md:52 (INV:14) | Reword the definition to "a `gh api` call whose method is not GET" and ship it with M-03 (INV:14, INV:22). |
| M-19 | INV-014 (MEDIUM, interaction_effects): Task 5's quoted-phrase rule (TL:104-105) can collide with TL:22's no-copy rule for WC-12, WC-13 and heartbeats, and with TL:46's ban on a fixed heartbeat cadence | should-fix | none | **no** | TL:22, TL:46, TL:104-105, SRC:59 (INV:18) | Say "a phrase", exempt the worker-session duties from verbatim copying, and name the phrase to pin for WC-12, WC-13 and heartbeats; word M-05's fix to match (INV:18). |

Run conditions (not plan defects; they go to `run_conditions`, not to `findings`):

| ID | Condition | Why it is a run condition | Citation |
|---|---|---|---|
| INV-005 (MEDIUM) | The agreed plan fixes must be made by hand, or by a fresh `/sc:workflow` package, before the first `T<id>: start` line of `/sc:implement`. After that line any plan change is `E-PLAN-CHANGED` with no repair. | It depends on who edits the plan and when, not on the plan text; the workflow may not edit the plan from reflect findings. | INV:9; `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:43` (opened) |
| INV-007 (MEDIUM) | Run the plan with no other writer in this worktree, or in its own worktree. Other sessions have uncommitted edits here, and a sibling commit halts the run on `head-moved`. | It depends on the execution environment, not on the plan text; non-cooperating writers are unsupported. | INV:11; managed-workspace.md:85 (opened); qa.md:280 |

Probe items not entered as findings:

| ID | Status, severity | Why not entered | Where it is reflected |
|---|---|---|---|
| INV-011 | UNADDRESSED, LOW | LOW needs no action under the gate (SK:1467) | Optional clause on M-12: also assert the scan found at least 45 command files (INV:15) |
| INV-015 | UNADDRESSED, LOW | LOW | Wording note on M-02 and M-05: pin path-free phrases (INV:19) |
| INV-016 | UNADDRESSED, LOW | LOW | Wording note on M-05: put the phrase rule in Tasks 1-2 (INV:20) |
| INV-017 | UNADDRESSED, LOW | LOW | Optional wording on M-01: "no command source file under `src/superclaude/commands/`" (INV:21) |
| INV-003, 004, 006, 008, 009, 012, 013, 018 | ADDRESSED, LOW | Already handled by the debate or holding today (INV:25) | INV-003 supports M-15; INV-009 supports M-03's matcher rule; INV-018 ties M-03 to M-18 |

All ten UNADDRESSED items (including the four LOW ones and the two run conditions) are listed in `unaddressed_invariants`, as the schema requires.

## (c) Changes NOT Being Made (with rationale)
| Diff point | Rejected approach (proposed by) | Rationale |
|---|---|---|
| X-001, S-001 | Keep the PASS verdict (A, B) | Lost 3-0; both PASS advocates conceded (R1a:36, R1b:35) |
| C-001 | Grade the Task 6 phase slot blocking (B) | Decided 2-1 for should-fix: only the Task 6 review can catch it, because the FINAL list has no task-instruction breach (R2c:56, qa.md:310), and a true "none" can fill the slot (R2a:59). B accepts should-fix as a fallback (R2b:64). Dissent kept in M-03. |
| U-003 | R2-1 at should-fix (B's card, C in Round 1) | Plan text is not "delivered text or code" (qa.md:50), so no gate can act on it (R2b:17, R2c:23) |
| C-005 | R3-F6 at minor (A in Round 1) | A withdrew; it costs a repair round like R1-F2 (R2a:21) |
| U-008 | Fold R3-F4 into R1-F5 (A in Round 1) | A withdrew; a FINAL route exists if the copy is added (R2a:15) |
| X-003 | R3-F2 at minor (offered by C in Round 1) | All three keep should-fix in Round 2 (R2a:98, R2b:110, R2c:25) |
| C-003 | "Task 5's only way out is to edit WORKER-CONTRACT.md" (VC:55-57) | Withdrawn: adding a spec phrase breaks no Task 1-2 AC (R2c:13, R2a:48) |
| C-001 | Agent hits as write verbs (VC:97-99) and learning-guide "write verbs" (R2a:13) | False matches ("through practical"); `git merge-base` is read-only (R2b:40, R2c:19) |
| C-001 | Fixed hit counts (40 `gh pr`, about 121 sites) as checkable numbers | Counts depend on the matcher (R2c:19; INV:13); the fix names the matcher instead |
| C-002 | "two tests pin plugin core copies" (VA:95) | Only one test reads the copy (R1a:47, R2a:19) |
| C-005 | Line-290 citation for the heading slice (VC:123) | Wrong line; replaced by 341, 819 and 1091 (R1c:44, R2c:15) |
| S-005 | B's matrix_omissions as a finding | Bookkeeping; kept as a note (R2a:82, R2b:93, R2c:87) |
| S-008 | A Task 7 environment finding | The paths exist today (R1b:31; INV:10); note only (R2a:83, R2b:94, R2c:88) |
| C-002 | R2-3 as a standalone finding (B) | Subsumed by R1-F5 (R2b:15) |
| (probe) | INV-005 and INV-007 as plan defects | They depend on how the plan is run, not its text (INV:9, INV:11); kept as run conditions |
| (probe) | INV-011, INV-015, INV-016, INV-017 as findings | LOW; no gate action (SK:1467); kept as wording notes on M-01, M-02, M-05 and M-12 |

## (d) merged-verdict.yaml Schema
Required top-level keys, in this order:

| Key | Type | Value for this merge |
|---|---|---|
| `merge_method` | string, fixed | `adversarial` |
| `verdict` | `PASS` or `FAIL` | `FAIL` (any blocking finding, adjudicated or not, makes it FAIL) |
| `base_variant` | map: `id`, `file`, `reviewer`, `persona`, `score` | Variant A, `variant-1-original.md`, 1, analyzer, 0.929 |
| `convergence_score` | float 0.00-1.00 | `1.00` |
| `convergence_status` | `CONVERGED`, `NOT_CONVERGED`, `BLOCKED_BY_TAXONOMY` or `BLOCKED_BY_INVARIANTS` (SK:1492-1496) | `BLOCKED_BY_INVARIANTS` |
| `blocking_count` | integer = number of `findings` with `severity: blocking` | `2` |
| `findings` | list of finding maps (fields below) | M-01 to M-19 |
| `unaddressed_invariants` | list of maps with exactly `id`, `category`, `assumption`, `severity` | the 10 UNADDRESSED probe rows |
| `run_conditions` | list of maps: `id`, `condition`, `source` | INV-005, INV-007 |
| `rejected_changes` | list of maps: `diff_point`, `rejected`, `proposed_by`, `reason` | the rows of section (c) |
| `provenance` | map | see below |

Finding fields: `id` (M-NN), `topic` (diff-analysis ids), `card_items` (list), `title`, `severity` (`blocking`, `should-fix` or `minor`), `deviation_class` (`authorized`, `necessary`, `drift`, `regression` or `none`), `tasks` (plan task numbers; 0 = Constraints), `adjudicated` (bool), `source` (`debate` or `invariant-probe`), `debate` (`agreement`, `confidence`, `dissent`; null when not adjudicated), `reviewers` (list of `reviewer`, `variant`, `calibrated_confidence`), `citations` (list of `TL:N`, `SRC:N`, `qa.md:N` or repo paths), `fix` (one line), `can_halt` (string or null).

Target content for the merge executor (values are final; only whitespace may change):

```yaml
merge_method: adversarial
verdict: FAIL
base_variant:
  id: A
  file: variant-1-original.md
  reviewer: 1
  persona: analyzer
  score: 0.929
convergence_score: 1.00
convergence_status: BLOCKED_BY_INVARIANTS
blocking_count: 2
findings:
  - id: M-01
    topic: [X-002, U-006]
    card_items: [R3-F1]
    title: "Constraint TL:21 forbids skill-file edits; Task 4 must overwrite a file inside the sc-recommend skill package"
    severity: blocking
    deviation_class: drift
    tasks: [4]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.90, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:21", "TL:24", "TL:90", "TL:93", "SRC:220", "qa.md:52", "qa.md:61", "qa.md:310", "qa.md:286"]
    fix: "Reword TL:21: P0 edits no command file, no SKILL.md and no agent file; the only file written under a skills directory is the byte-for-byte copy of HOW-WE-WORK.md in plugins/superclaude/skills/sc-recommend/refs/ that Task 4 makes."
    can_halt: "Task 4 QA (B4) or managed FINAL (violated Constraint); no repair satisfies both TL:21 and TL:93"
  - id: M-02
    topic: [U-001]
    card_items: [R1-F4]
    title: "Installed-path rule missing from Constraints; a literal restatement ships src/superclaude paths and evidence ids into an installed core file"
    severity: should-fix
    deviation_class: none
    tasks: [1, 2]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.80, dissent: null}
    reviewers: [{reviewer: 1, variant: A, calibrated_confidence: 0.86}]
    citations: ["TL:17-27", "TL:22", "TL:37", "SRC:59"]
    fix: "Add a Constraints line: WORKER-CONTRACT.md and the HOW-WE-WORK.md section use installed ~/.claude/ paths only and copy no CAPS:/INV- ids or src/superclaude/ paths."
    can_halt: null
  - id: M-03
    topic: [C-001]
    card_items: [R1-F3, R3-F5]
    title: "Task 6 requires a converting phase for every allowlisted hit; many hits have none, some are read-only or false matches, and keys are unspecified"
    severity: should-fix
    deviation_class: drift
    tasks: [6]
    adjudicated: true
    source: debate
    debate: {agreement: "majority 2-1", confidence: 0.65, dissent: "Variant B advocate: blocking, can halt through the Task 6 review (0.60); accepts should-fix in the same revision as fallback"}
    reviewers: [{reviewer: 1, variant: A, calibrated_confidence: 0.86}, {reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:125", "SRC:61", "SRC:201", "SRC:224", "SRC:305"]
    fix: "Replace TL:125's two-way rule with five categories (WC-9 allowed; refused or deferred in a named phase; never a worker; no command converts this file; read-only or false match), key by path, verb and stripped line text, scan with word boundaries; ship with M-18."
    can_halt: "Task 6 review only"
  - id: M-04
    topic: [X-003, U-007]
    card_items: [R3-F2]
    title: "Constraint TL:22 limits the contract to sections 2.1-2.3 while Task 2 adds section 3.1 flags and a section 6 marker"
    severity: should-fix
    deviation_class: drift
    tasks: [2]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.80, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:22", "TL:58", "SRC:59", "SRC:84", "SRC:220"]
    fix: "Add to TL:22: plus, in the brief template only, the section 3.1 Brief-must-pass flags and the section 6 phase markers (--report-dir from P1)."
    can_halt: "Task 2 QA or managed FINAL, for the 'from P1' marker only"
  - id: M-05
    topic: [C-003]
    card_items: [R1-F1, R3-F3]
    title: "Task 5 must pin 'at most 10' 'as written in section 2.3', but the spec says 'maximum of 10 inputs'; Tasks 1-2 need not supply quotable phrases"
    severity: should-fix
    deviation_class: drift
    tasks: [1, 2, 5]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.92, dissent: null}
    reviewers: [{reviewer: 1, variant: A, calibrated_confidence: 0.86}, {reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:56", "TL:104", "TL:112", "SRC:122"]
    fix: "Use the spec's 'maximum of 10 inputs' / 'never exceeds 10' in TL:56 and TL:112 and drop '(as written in section 2.3)'; Tasks 1-2 record the phrase each rule is tested on, worded per M-19."
    can_halt: null
  - id: M-06
    topic: [U-002]
    card_items: [R1-F2]
    title: "Task 8 needs an evidence file for each of 11 checks; no task saves files for AC-0.1, AC-0.2, AC-0.3"
    severity: should-fix
    deviation_class: none
    tasks: [1, 3, 4, 8]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.75, dissent: null}
    reviewers: [{reviewer: 1, variant: A, calibrated_confidence: 0.86}]
    citations: ["TL:47", "TL:72", "TL:93-94", "TL:147-152", "TL:157", "qa.md:85"]
    fix: "In Task 8, re-run AC-0.1, AC-0.2, AC-0.3, AC-C1 and AC-C2 and save each output to ./artifacts/<id>.txt as the report's evidence."
    can_halt: null
  - id: M-07
    topic: [U-008]
    card_items: [R3-F4]
    title: "An added plugin core copy of WORKER-CONTRACT.md has no sync check"
    severity: should-fix
    deviation_class: none
    tasks: [3, 5]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.70, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:69", "TL:74", "qa.md:310"]
    fix: "If Task 3 adds the copy, Task 5 asserts it is byte-identical to the src file (pattern: test_plugin_mirror_matches_src)."
    can_halt: null
  - id: M-08
    topic: [C-005]
    card_items: [R3-F6]
    title: "Routing-guide tests (ASCII only; fixed heading slices) constrain the new Orca section"
    severity: should-fix
    deviation_class: none
    tasks: [4]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.90, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:90", "TL:93", "tests/core/test_how_we_work_routing_table.py:341", "tests/core/test_how_we_work_routing_table.py:819", "tests/core/test_how_we_work_routing_table.py:1091"]
    fix: "Add to Task 4: the new section is ASCII only and is a new top-level section after the last one, outside the level-table and routing markers."
    can_halt: null
  - id: M-09
    topic: [C-002, X-004]
    card_items: [R1-F5, R2-3]
    title: "Task 3 does not name the evidence that decides the plugin copy"
    severity: minor
    deviation_class: none
    tasks: [3]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.92, dissent: null}
    reviewers: [{reviewer: 1, variant: A, calibrated_confidence: 0.86}, {reviewer: 2, variant: B, calibrated_confidence: 0.82}]
    citations: ["TL:69", "SRC:252", "scripts/build_superclaude_plugin.py:75", "tests/commands/test_routing_plugin_parity.py:3", "tests/commands/test_impact_command.py:309"]
    fix: "Name build-script line 75, the parity test, the one test that reads a plugin core copy, and SRC:252's by-name exclusion in Task 3."
    can_halt: null
  - id: M-10
    topic: [U-003]
    card_items: [R2-1]
    title: "Constraints cite AC-0.8, which does not exist"
    severity: minor
    deviation_class: drift
    tasks: [0]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.75, dissent: null}
    reviewers: [{reviewer: 2, variant: B, calibrated_confidence: 0.82}]
    citations: ["TL:19", "SRC:304-306"]
    fix: "Delete the AC-0.8 sentence or replace it with 'the P1 checks are AC-1.1 to AC-1.8 (section 7.3)'."
    can_halt: null
  - id: M-11
    topic: [U-004, U-012]
    card_items: [R2-2, R3-F10]
    title: "No handoff of static results into the live plan's phase report; re-staging omitted from next steps"
    severity: minor
    deviation_class: none
    tasks: [8]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.75, dissent: null}
    reviewers: [{reviewer: 2, variant: B, calibrated_confidence: 0.82}, {reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:19", "TL:154", "SRC:238", "SRC:303-304"]
    fix: "End the static report with a 'results the P0 live plan must cite' list and add the coordinator's re-staging of .dev/tasks and AC-C4 re-run to the next steps."
    can_halt: null
  - id: M-12
    topic: [U-009]
    card_items: [R3-F7]
    title: "Hard-coded negative check for Unattended mode sections"
    severity: minor
    deviation_class: none
    tasks: [5]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.90, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:115", "SRC:306"]
    fix: "Write it as a cumulative per-phase map, {'P0': set()}; optionally also assert at least 45 command files were scanned (INV-011)."
    can_halt: null
  - id: M-13
    topic: [U-010]
    card_items: [R3-F8]
    title: "Brief-template flags are not checked against the command files"
    severity: minor
    deviation_class: none
    tasks: [2, 5]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.90, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:58"]
    fix: "In Task 5, assert each template flag exists in its command file, except the flags marked 'from P1'."
    can_halt: null
  - id: M-14
    topic: [U-011]
    card_items: [R3-F9]
    title: "Goal says every copy gets the Orca section; Task 4 leaves the CLAUDE.md copy unchanged"
    severity: minor
    deviation_class: none
    tasks: [4]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.90, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:15", "TL:90"]
    fix: "Reword the Goal: the Orca section is in HOW-WE-WORK.md and its plugin copy; the CLAUDE.md level-table copy is unchanged."
    can_halt: null
  - id: M-15
    topic: [C-004]
    card_items: [R3-F11]
    title: "No make verify-sync baseline; tests/docs and tests/unit not in the wider baseline"
    severity: minor
    deviation_class: none
    tasks: [1, 4]
    adjudicated: true
    source: debate
    debate: {agreement: unanimous, confidence: 0.92, dissent: null}
    reviewers: [{reviewer: 3, variant: C, calibrated_confidence: 0.88}]
    citations: ["TL:33-35", "TL:96"]
    fix: "In Task 1 also save make verify-sync output, and add tests/docs and tests/unit to the wider baseline and Task 4's comparison."
    can_halt: null
  - id: M-16
    topic: [INV-001]
    card_items: []
    title: "Task 1's wider baseline already has 8 failures; the managed FINAL can read the cited log as a failure and block archiving"
    severity: blocking
    deviation_class: none
    tasks: [1, 4]
    adjudicated: false
    source: invariant-probe
    debate: null
    reviewers: []
    citations: ["TL:35", "TL:48", "TL:95", "qa.md:310", "qa.md:294", "qa.md:286"]
    fix: "In TL:35 and TL:95 state that pre-existing failures are expected, list the 8 failing test ids as the accepted baseline, and cite the per-test comparison file rather than the raw log."
    can_halt: "managed FINAL (E-ARCHIVE-BLOCKED), depending on whether the FINAL follows qa.md:310 or qa.md:294"
  - id: M-17
    topic: [INV-002]
    card_items: []
    title: "The wider test run rewrites a tracked perf.json, which enters Task 1 and Task 4 diffs"
    severity: should-fix
    deviation_class: none
    tasks: [1, 4, 8]
    adjudicated: false
    source: invariant-probe
    debate: null
    reviewers: []
    citations: ["TL:35", "TL:95", "TL:154", "qa.md:51"]
    fix: "Add --deselect tests/cli/eval/test_perf_home_setup.py to the wider runs, or git restore .dev/releases/current/cliEval/evidence/T02.15/perf.json after each run."
    can_halt: null
  - id: M-18
    topic: [INV-010]
    card_items: []
    title: "TL:125 counts -f/-F as a gh api post, so GET reads that pass -F are posts under the plan"
    severity: should-fix
    deviation_class: drift
    tasks: [6]
    adjudicated: false
    source: invariant-probe
    debate: null
    reviewers: []
    citations: ["TL:125", "SRC:305", "qa.md:50", "qa.md:52"]
    fix: "Define a gh api post as a gh api call whose method is not GET; ship with M-03."
    can_halt: null
  - id: M-19
    topic: [INV-014]
    card_items: []
    title: "Task 5's quoted-phrase rule can collide with TL:22's no-copy rule for WC-12, WC-13 and heartbeats"
    severity: should-fix
    deviation_class: none
    tasks: [1, 2, 5]
    adjudicated: false
    source: invariant-probe
    debate: null
    reviewers: []
    citations: ["TL:22", "TL:46", "TL:104-105", "SRC:59"]
    fix: "Say 'a phrase', exempt the worker-session duties from verbatim copying, and name the phrase to pin for WC-12, WC-13 and heartbeats."
    can_halt: null
unaddressed_invariants:
  - {id: INV-001, category: sufficiency_challenge, assumption: "Fixing R3-F1 and the should-fixes is enough for per-task QA and the managed FINAL to pass", severity: HIGH}
  - {id: INV-002, category: state_variables, assumption: "Running the plan's test commands changes no tracked file", severity: MEDIUM}
  - {id: INV-005, category: state_variables, assumption: "Someone applies the agreed plan fix before execution", severity: MEDIUM}
  - {id: INV-007, category: state_variables, assumption: "Only the executor writes in this worktree during the run", severity: MEDIUM}
  - {id: INV-010, category: interaction_effects, assumption: "The merged Task 6 category 'read-only or a false match' fits the plan's definition of a gh api post", severity: MEDIUM}
  - {id: INV-011, category: collection_boundaries, assumption: "The P0 'no Unattended mode section' assertion checks something real", severity: LOW}
  - {id: INV-014, category: interaction_effects, assumption: "Task 5's quoted-phrase rule is compatible with TL:22 for the worker-session duties", severity: MEDIUM}
  - {id: INV-015, category: interaction_effects, assumption: "The installed-path Constraint and the quoted-phrase rule can both be met", severity: LOW}
  - {id: INV-016, category: interaction_effects, assumption: "Task 5 can safely add missing spec phrases to WORKER-CONTRACT.md", severity: LOW}
  - {id: INV-017, category: interaction_effects, assumption: "Rewording TL:21 to 'P0 edits no command file' creates no new literal breach", severity: LOW}
run_conditions:
  - id: INV-005
    condition: "Apply the plan fixes by hand, or through a fresh /sc:workflow package, before the first T<id>: start line; any later plan change stops the run with E-PLAN-CHANGED."
    source: ["invariant-probe.md:9", "managed-workspace.md:43"]
  - id: INV-007
    condition: "Run /sc:implement with no other writer in this worktree, or in its own worktree; a sibling commit halts the run on head-moved."
    source: ["invariant-probe.md:11", "managed-workspace.md:85", "qa.md:280"]
rejected_changes:
  - {diff_point: "X-001/S-001", rejected: "Keep the PASS verdict", proposed_by: [A, B], reason: "Lost 3-0; both advocates conceded"}
  - {diff_point: C-001, rejected: "Grade the Task 6 phase slot blocking", proposed_by: [B], reason: "Decided 2-1 for should-fix; only the Task 6 review can catch it; dissent kept in M-03"}
  - {diff_point: U-003, rejected: "R2-1 at should-fix", proposed_by: [B, C], reason: "Plan text is not delivered text; no gate can act on it"}
  - {diff_point: C-005, rejected: "R3-F6 at minor", proposed_by: [A], reason: "Withdrawn by A in Round 2"}
  - {diff_point: U-008, rejected: "Fold R3-F4 into R1-F5", proposed_by: [A], reason: "Withdrawn by A; a FINAL route exists if the copy is added"}
  - {diff_point: X-003, rejected: "R3-F2 at minor", proposed_by: [C], reason: "All three kept should-fix in Round 2"}
  - {diff_point: C-003, rejected: "Task 5's only way out is to edit the contract", proposed_by: [C], reason: "Withdrawn; adding a phrase breaks no Task 1-2 AC"}
  - {diff_point: C-001, rejected: "Agent and learning-guide hits as write verbs", proposed_by: [A, C], reason: "False matches; git merge-base is read-only"}
  - {diff_point: C-001, rejected: "Fixed hit counts as checkable numbers", proposed_by: [C], reason: "Counts depend on the matcher; the fix names the matcher"}
  - {diff_point: C-002, rejected: "Two tests pin plugin core copies", proposed_by: [A], reason: "Only one test reads the copy"}
  - {diff_point: C-005, rejected: "Line-290 citation for the heading slice", proposed_by: [C], reason: "Wrong line; replaced by 341, 819, 1091"}
  - {diff_point: S-005, rejected: "matrix_omissions as a finding", proposed_by: [B], reason: "Bookkeeping; kept as a note"}
  - {diff_point: S-008, rejected: "A Task 7 environment finding", proposed_by: [], reason: "Paths exist today; note only"}
  - {diff_point: C-002, rejected: "R2-3 as a standalone finding", proposed_by: [B], reason: "Subsumed by R1-F5"}
  - {diff_point: probe, rejected: "INV-005 and INV-007 as plan defects", proposed_by: [], reason: "Run conditions, not plan text"}
  - {diff_point: probe, rejected: "LOW invariants as findings", proposed_by: [], reason: "LOW needs no gate action; kept as wording notes"}
provenance:
  produced_by: "sc:adversarial Mode A, depth standard, non-interactive"
  orchestrator: debate-orchestrator
  plan: ".dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md"
  spec: ".dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md"
  variants:
    A: {file: variant-1-original.md, reviewer: 1, persona: analyzer, card_verdict: PASS, calibrated_confidence: 0.86, base_score: 0.929}
    B: {file: variant-2-original.md, reviewer: 2, persona: qa, card_verdict: PASS, calibrated_confidence: 0.82, base_score: 0.829}
    C: {file: variant-3-original.md, reviewer: 3, persona: refactorer, card_verdict: FAIL, calibrated_confidence: 0.88, base_score: 0.809}
  rounds: {completed: 2, round_2_5: ran, round_3: "skipped (depth standard)"}
  convergence: {agreed: 21, total: 21, threshold: 0.80, taxonomy: "L1 4, L2 6, L3 11; all covered", gate: "INV-001 HIGH UNADDRESSED"}
  blocking_count_basis: {adjudicated: 1, not_adjudicated: 1, ids: [M-01, M-16]}
  artifacts: [diff-analysis.md, debate-transcript.md, invariant-probe.md, base-selection.md, refactor-plan.md]
  notes:
    - "Variant B's matrix_omissions (source.md:236, source.md:188) kept as a coverage-matrix note"
    - "Grounding hunk H4 (build_superclaude_plugin.py) was empty in the reflect run; evidence gap, not a plan defect"
    - "Task 7 environment checked by Variant A's self-audit and re-confirmed by the probe (INV-006)"
    - "The probe's test run rewrote and then restored a tracked perf.json (INV-002 method note)"
  approval: {status: auto-approved, approved_by: auto, timestamp: "2026-11-03T07:14:21Z"}
```

## Risk Summary
| Change # | Risk | Impact if it fails | Rollback |
|---|---|---|---|
| 1 | Medium | The merged card would keep the base's PASS against a 3-0 debate result | Restore `verdict` from VC:4 and re-insert M-01 |
| 2 | Medium | A fix without M-18 leaves the GET-read conflict open (INV:22) | Merge M-03 and M-18 as one plan edit |
| 3 | Low | A fix that says "copy the spec's wording" collides with TL:22 and TL:46 (INV:18) | Re-word per M-19 |
| 4 | Low | The base's wrong "two tests" claim would survive | Re-apply the correction from R1a:47 |
| 5-7 | Low | Additive; a missing item loses coverage only | Re-append from the cited card lines |
| 8 | Medium | Unadjudicated findings could be read as debated | Keep `adjudicated: false` and `source: invariant-probe` on M-16 to M-19 |
| 9 | Low | Run conditions lost from the record | Re-add from INV:9 and INV:11 |
| 10 | Low | Schema check fails on a missing key | Re-fill from section (d) |

## Review Status
- [x] Auto-approved (default; the run is not interactive)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-03T07:14:21Z
