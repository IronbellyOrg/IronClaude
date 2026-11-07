# Refactoring Plan: Merge into Base (Variant 2)

Paths are relative to the repo root. "plan:N" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`; "src:N" = `source.md` in the same folder; "spec:N" = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; "SKILL" = `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`; "routing" = its `refs/handoff-routing.md`; "cmd" = `src/superclaude/commands/brainstorm.md`; "a1/a2/a3:N" = lines of `rounds/round2-advocate-1/2/3.md` as cited in `debate-transcript.md`. Every file:line in the "Replacement wording" section was Read for this plan.

## Overview

- Base: Variant 2 (reviewer 2, qa, haiku slot); combined 0.815, tiebreaker applied (V1 0.783 within 5%; V2 wins on debate points 5.83 vs 4.83). See `base-selection.md`.
- Incorporating strengths from: Variant 1 (analyzer, sonnet), Variant 3 (refactorer, opus).
- Output to be written by the merge executor: ONE consolidated verdict card (reviewer-card schema) whose findings are exactly the "Final consolidated finding list" below, in that order, with the priorities given there. The executor does not re-decide any priority or wording.
- Planned changes: 12 (Changes 1-12).
- Risk level: Medium overall (Change 1 carries new remedy text that no advocate proposed verbatim).
- Convergence status carried forward: BLOCKED_BY_INVARIANTS (INV-020 open, see the disposition section). The merged card must carry INV-020 as an open conflict, not as resolved.

## Planned Changes

### Change 1: Add the Task 6 tier-wording defect as a P1 finding (from Variant 3)
- **Source**: V3, R3-1 (`variant-3-original.md:7-11`), diagnosis only; widened by a3 New evidence 1.
- **Target**: Base, new finding inserted first (M-01) (insert).
- **Rationale**: C-007 winner V3, unanimous, 92%; X-003 winner V3, unanimous, 92% (Round 2). All three advocates agree a clean `/sc:analyze` run is also `primary` (SKILL:187,198), and a3 showed the same sentence is wrong for `fallback_1` too. V3's remedy (decide by `source`) is NOT incorporated: `source` is only `codebase | research-light | research-deep` (SKILL:372; a3 criticism 1, conceded).
- **Integration point**: M-01 claim = V3's diagnosis widened to both tiers; remedy = the "Replacement wording" section of this plan.
- **Risk**: Medium. The remedy text is the orchestrator's synthesis of a1:52, a2:34 and a3:69 after the invariant probe; no advocate signed it verbatim.

### Change 2: Give base R2-1 its remedy and capture point (from Variant 1)
- **Source**: V1, R1-2 (`variant-1-original.md:12-16`); capture point from INV-001.
- **Target**: Base R2-1 (M-02) (replace remedy; drop "doubly").
- **Rationale**: C-001 split (V2 diagnosis + V1 remedy), unanimous, 95%; X-005 winner V2 with "doubly overreaches", unanimous, 95%; A-002 QUALIFY 93% and A-004 QUALIFY 96% (capture baselines at run time).
- **Integration point**: M-02 remedy text as given in the final list.
- **Risk**: Low. Adds one step to Task 1 and rewrites one Task 7 bullet.

### Change 3: Sharpen base R2-3 to the paragraph boundary (from Variant 3)
- **Source**: V3, R3-3 first half; a3 Proposed wording "Pins (Tasks 4-5)".
- **Target**: Base R2-3 (M-04) (replace claim and add remedy).
- **Rationale**: C-002 winner V3, unanimous, 96%; X-001 split (V2+V3), unanimous, 95%.
- **Integration point**: M-04.
- **Risk**: Low.

### Change 4: Add per-tier scoping of the routing pins (from Variants 1 and 3)
- **Source**: V1 R1-3 (`variant-1-original.md:17-21`); V3 R3-3 second half.
- **Target**: Base, new finding M-05 (insert after M-04).
- **Rationale**: C-005 split (V1+V3), unanimous, 95%. INV-009 confirms the `grep -c ... prints 2` smoke check still holds with the longer phrase.
- **Integration point**: M-05.
- **Risk**: Low.

### Change 5: Add the placement decision to base R2-4 (from Variants 1 and 3)
- **Source**: V1 R1-8 (`variant-1-original.md:42-46`); V3 R3-5 (`variant-3-original.md:27-31`); INV-017 and INV-021 for the AC consequences.
- **Target**: Base R2-4 (M-07) (append remedy).
- **Rationale**: C-006 and X-004 split (V1 defensible + V3 placement), unanimous, 90%. The debate allowed "7.2 step 4 or the P1 rows" (a1:58; a3:73). This plan picks 7.2 step 4 because INV-021 requires a place every later live-plan author reads, and src:9's stated goal is "where the P2 live plan author will find it". This departs from src:9's literal second branch ("a note in the P1 section") and must be recorded in the plan as a Necessary deviation.
- **Integration point**: M-07.
- **Risk**: Medium. Two spec lines change instead of one, so Task 6's AC must change with it (INV-017(b)).

### Change 6: Pin both halves of the owner rule (from Variants 1 and 3, onto base R2-2)
- **Source**: V1 R1-4 remedy shape; V1 Round 2 New evidence (d); V3 Round 2 New evidence 5; V3 R3-6 shared phrase (C-012).
- **Target**: Base R2-2 (M-03) (append remedy).
- **Rationale**: C-004 winner V2, unanimous, 94% (priority P1 held by V2; V1 conceded its P2 rating, a1 criticism 4). C-012 winner V3, unanimous, 91%.
- **Integration point**: M-03 remedy = the shared phrases fixed in "Replacement wording" (Tasks 1-3 rule and pins).
- **Risk**: Low.

### Change 7: Replace the hard-coded count in base R2-7 by a recorded before-count (from Variants 1 and 3)
- **Source**: V1 R1-6; V3 R3-7.
- **Target**: Base R2-7 (M-08) (replace remedy; keep 17 as today's value).
- **Rationale**: C-008 split (V2 number + V1/V3 method), unanimous, 93%; INV-008 (the count after the edit depends on how many phrases are added).
- **Integration point**: M-08.
- **Risk**: Low.

### Change 8: Add the section-label error (from Variant 3)
- **Source**: V3, R3-4 (`variant-3-original.md:22-26`).
- **Target**: Base, new finding M-11.
- **Rationale**: C-011 winner V3, unanimous, 98%; U-003 Medium.
- **Integration point**: M-11.
- **Risk**: Low.

### Change 9: Add the Task 7 "do not edit any file" wording fix (from Variant 1)
- **Source**: V1, R1-10 first half (`variant-1-original.md:52-56`).
- **Target**: Base, new finding M-13.
- **Rationale**: U-006 Low; not contested in either round. The second half of R1-10 is already base R2-6 (C-009).
- **Integration point**: M-13.
- **Risk**: Low.

### Change 10: Add the failed-call ambiguity of plan:30 (from Variant 3, reframed)
- **Source**: V3 R3-9 as reframed in Round 2 (a3 criticism 10); V2 Round 2 caveat on "ran" (debate-transcript.md:394).
- **Target**: Base, new finding M-14.
- **Rationale**: U-005 Low; a3 kept it "as Low, reframed". WC-4 writes a contract "on success, failure, blocked and partial outcomes" (spec:72), so "only for a nested command that ran" can be read to unlist a failed call's contract.
- **Integration point**: M-14, resolved by the Tasks 1-3 wording rule.
- **Risk**: Low.

### Change 11: Add the plugin-mirror resolution point for brief item 3 (from Variant 1)
- **Source**: V1, R1-8 last sentence (spec line 443).
- **Target**: Base, new finding M-17.
- **Rationale**: V2 has no finding on brief item 3 (Completeness 1 NOT MET in `base-selection.md`). spec:443 (open item 8) says "Each phase's plan must resolve this before editing"; plan:21 already decides "It is not edited by this plan" but does not say that this is the resolution of item 8. Not a scored debate point, so it is carried at P2 Low with V1's own evidence.
- **Integration point**: M-17.
- **Risk**: Low.

### Change 12: Add the probe-derived plan fixes that the replacement wording needs
- **Source**: invariant-probe.md INV-002, INV-005, INV-016 (UNADDRESSED, MEDIUM/LOW).
- **Target**: Base, new findings M-15, M-16, and an extra assertion inside M-04.
- **Rationale**: Each changes plan text that the merged card would otherwise leave wrong; see "Invariant probe disposition".
- **Integration point**: M-04 (INV-005), M-15 (INV-016), M-16 (INV-002).
- **Risk**: Low.

## Base weaknesses and the better variant for each

| Base (V2) weakness | Evidence | Better variant | Handled by |
|---|---|---|---|
| Silent on the Task 6 tier wording (C-007/X-003), the defect that reproduces lc10 in reverse | a2 criticism 1 (conceded) | V3 (diagnosis); remedy from this plan | Change 1 |
| R2-1 names no remedy | a2 criticism 2 (conceded) | V1 (R1-2 before/after diff) | Change 2 |
| R2-1 "doubly unpassable" overreaches | X-005, a2 criticism 3 | V1 (single-clause reading) | Change 2 |
| R2-3 does not say Task 1's clause is unpinned | C-002, X-001 | V3 | Change 3 |
| R2-6 diagnoses the file-wide count but gives no fix | a2 criticism 8 (conceded) | V1 (R1-3, `_section` helper) | Change 4 |
| R2-4 names no placement | a2 criticism 5 (conceded) | V1 + V3 split | Change 5 |
| R2-7 fixes the count at 17 then 18 | A-004, INV-008 | V1 / V3 (record the before-count) | Change 7 |
| Missed C-011 (section 3.1 vs section 6) | a2 criticism 7 (conceded) | V3 | Change 8 |
| Missed C-012 (verb forms) | C-012 | V3 | Change 6 |
| No finding on brief item 3 (plugin mirror) | `base-selection.md` Completeness 1 | V1 (R1-8, spec:443) | Change 11 |

## Final consolidated finding list

Card verdict to write: "The plan covers the five brief items but is not ready for `/sc:implement`: three P1 fixes (M-01, M-02, M-03) and the P2 edits below are needed first. The Tier-1 card's 'ready after one fix (F-1)' is rejected. INV-020 is an open conflict for the owner and the P2 live-plan author (M-18)." Calibrated confidence for the merged card: not re-calibrated here; the inputs were 0.85 / 0.82 / 0.82.

| ID | Priority | Severity | Claim (what is wrong) | Required plan change | Evidence | Debate basis |
|---|---|---|---|---|---|---|
| M-01 | P1 | High | Task 6's live-check sentence ("a `primary` or `fallback_1` scan is recorded as the tier used, with no nested folder") decides the folder by `quality_tier`. Tier does not decide it: a clean `/sc:analyze` run is also `primary` (SKILL:187,198), and no field of `enrichment_used` names the tool (SKILL:372). A checker following it fails a correct analyze run, which is lc10 in reverse. | Replace plan:81's second sentence with the exact sentence in "Replacement wording" (live-check sentence), and its first sentence with the companion sentence there. Record in the plan that both depart from src:9's sketch on purpose (Necessary deviation). | plan:81; SKILL:187,195,198,372; src:9 | C-007 V3 92%; X-003 V3 92% |
| M-02 | P1 | High | Task 7 bullet 3 cannot pass: its first clause ("lists, among tracked paths, only the six files ... plus this package") fails on today's tree under any reading (950 staged `A` and 3 `R` under the archived P1 package; `git ls-files` = 953), and this package is untracked, so "plus this package" misdescribes it. The `.dev/tasks/done/` clause is reading-dependent. An infeasible AC reaches `E-HALT-QA`. | Task 1 gains a first step: before any edit, save `git status --porcelain` to `./artifacts/status-before.txt`. Task 7 saves `./artifacts/status-after.txt` and its bullet 3 becomes: "Every line that is in `./artifacts/status-after.txt` and not in `./artifacts/status-before.txt` names one of the six files in Constraints or a path under this package's folder; no such line names a path under `.claude/` or `plugins/`; and every line of `./artifacts/status-before.txt` that names a path under `.dev/tasks/done/` is unchanged in `./artifacts/status-after.txt`." The package-path exemption covers the `??` to `A` flip that `/sc:implement`'s `git add .dev/tasks` causes (INV-001). | plan:98; `artifacts/diagnostics.txt:3-7`; `sc-implement-protocol/refs/managed-workspace.md:36` | C-001 split V2+V1 95%; X-005 V2 95%; A-002, A-004 |
| M-03 | P1 | High | The owner rule has two halves (src:6: the fallback tier "writes no nested folder and lists no nested contract in artifacts"). No planned pin covers the contract half, and the conditional "exists only when `/sc:analyze` ran" is pinned only in the spec. An implementer can drop either from the three primitives and every planned check stays green. | Write Tasks 1-3 by the wording rule in "Replacement wording" and pin the shared phrases `no nested directory and no nested contract` and `` only by a `/sc:analyze` call `` in all three primitives (Task 4 for the skill and routing ref, Task 5 for the command file), as listed there. | src:6; plan:33,60,74 | C-004 V2 94%; C-012 V3 91% |
| M-04 | P2 | Medium | Task 4's new `fallback_1` assertion over the whole Wave 2A section passes on the old text (SKILL:199 holds `fallback_1` inside Wave 2A), contradicting plan:65. Task 1's paragraph clause is not vacuous (SKILL:195 lacks `fallback_1`) but is pinned by nothing. | Task 4 slices the paragraph that starts with the bold lead-in "Under `--unattended`" (up to the next blank line) and asserts `fallback_1`, `write no nested directory and no nested contract` and `` only by a `/sc:analyze` call `` in that slice, plus `"Quality-tier tracking" not in` the slice, so a slicer that returns the whole section fails (INV-005). Correct plan:65 to name the assertions that fail on the old text. | SKILL:195,197-199; `tests/skills/test_brainstorm_protocol.py:24-29`; plan:60,65 | C-002 V3 96%; X-001 V2+V3 95% |
| M-05 | P2 | Medium | The routing-ref checks are file-wide: `grep -c ... prints 2` (plan:42) and "at least twice" (plan:60) pass with both copies in one tier or in the research tiers. | Task 4 asserts each pinned phrase once in the Tier 1 slice (from the first `**Tier 1 (primary)**` to `**Tier 2 (fallback_1)**: codegraph`) and once in the Tier 2 slice (from there to `**Final fallback`), using the slicing pattern of `tests/skills/test_codegraph_adoption.py:56-59`. Keep the `grep -c` check as a smoke test (it still prints 2, INV-009). | plan:42,60; routing:16-33 | C-005 V1+V3 95% |
| M-06 | P2 | Medium | Task 7's test set omits `tests/skills/test_codegraph_adoption.py` (reads SKILL, routing, both `brainstorm.md` copies; its Tier 2 slice test spans the Task 2 edit) and `tests/skills/test_tier2_tavily_consistency.py` (reads SKILL). The one extra file it runs, `tests/commands/test_routing_plugin_parity.py`, reads none of the edited files. The planned text breaks neither omitted test (read, not run), so this is a coverage gap, not a missed break. | Add both files to Task 7's pytest command and to its AC bullet 2. | plan:93; `test_codegraph_adoption.py:20-23,75-82`; `test_tier2_tavily_consistency.py:19,49`; `test_routing_plugin_parity.py:16` | C-003 V1+V2 96%; C-013 V1+V2 93%; X-002 97%; A-001 ACCEPT 95% |
| M-07 | P2 | Medium | Task 6 puts a brainstorm-specific live-check instruction inside the general 2.1 bullet, and the plan never records that it evaluated src:9's placement rule. Spec 7.2 and 7.3 define no per-command extras (spec:281-327). | Keep the general (companion) sentence in the 2.1 bullet (spec:62), ending with a pointer "brainstorm's live-check extra for this is in 7.2 step 4". Append the live-check sentence to 7.2 step 4 (spec:286, after "At P0, AC-0.4 replaces this step."). Replace Task 6's AC with: the 2.1 bullet contains `only for a nested command that actually ran` and `7.2 step 4`; the 7.2 step 4 line contains `lc10`, `` a `source: codebase` entry `` and `` neither `quality_tier` nor `source` records ``; `git diff --stat` on the spec shows two lines changed. Do not pin `session file` (the spec already holds it many times, INV-017(a)). Record the departure from src:9's literal second branch as a Necessary deviation, reason: 7.2 step 4 is where every later live plan attaches its step-4 extras (INV-021). | plan:81,84-85; spec:62,281-327,376; src:9 | C-006 V1+V3 90%; X-004 V1+V3 90% |
| M-08 | P2 | Low | Task 5's "lists more cases than before the edit" has no recorded baseline. | Task 5 first saves the `--collect-only -q -k brainstorm` output to `./artifacts/t5-collect-before.txt`; AC: the count after the edit equals the before-count plus the number of phrases added (2 under M-03). 17 is today's value (`diagnostics.txt:11`), not a constant; no AC hard-codes 18 or 19 (INV-008). | plan:75; `diagnostics.txt:11`; `tests/skills/test_worker_contract.py:519-527,559-568` | C-008 V2+V1/V3 93% |
| M-09 | P2 | Low | Task 2 says each codebase tier list "ends with its `quality_tier` line"; the Tier 2 list ends with the Activation bullet (routing:31). | Task 2 places the Tier 1 bullet after routing:22 and the Tier 2 bullet after the Activation bullet (routing:31), both before `**Final fallback` (routing:33), so the Tier 2 bullet stays inside the slice `test_codegraph_adoption.py:75-82` reads. | routing:22,30-33; plan:39 | C-009 V1+V2 96% |
| M-10 | P2 | Low | Stale offsets: Task 4 says the test is at line 37 (it is at 39); Task 5 says the phrase list is at line 286 (the entry starts at 286, the list at 288). The brief's line-711 reference is a synthetic-section mutation and needs no change. | Correct both numbers; add one line to Task 5 saying line 711 needs no change. | `test_brainstorm_protocol.py:39`; `test_worker_contract.py:286-292,704-729` | C-010 V1+V2 94% |
| M-11 | P2 | Low | Task 6 calls spec line 142 "the `brainstorm` row of the section 6 table"; line 142 is in the section 3.1 table (spec:136-153), and section 6 starts at spec:215 (its brainstorm text is the P2 row, spec:222). | Say "the `brainstorm` row of the section 3.1 table (line 142)". | spec:136-142,215,222; plan:81 | C-011 V3 98% |
| M-12 | P2 | Low | `write no nested directory` (skill) is not a substring of `writes no nested directory` (routing, cmd), so each file is held to its own verb form. | Covered by M-03: the shared pinned phrase `no nested directory and no nested contract` is a substring of both forms. | plan:30,39,47 | C-012 V3 91% |
| M-13 | P2 | Low | Task 7 says "Do not edit any file in this task" but writes three logs under `./artifacts/`. | Say "Do not edit any source file in this task; it writes only the logs under `./artifacts/`." | plan:93 | U-006 (uncontested) |
| M-14 | P2 | Low | plan:30's new clause "a nested contract is listed in `artifacts` only for a nested command that ran" can be read as "succeeded" and would unlist a failed call's contract, which WC-4 writes on every outcome; cmd:157's unconditional "the nested contracts are listed in `artifacts`" is right. | Drop the clause; keep the skill's unconditional sentence, extended to "The nested contract is listed in `artifacts`, also when the call failed." (Tasks 1-3 rule). | plan:30; cmd:157; spec:72; `src/superclaude/commands/analyze.md:98` | U-005 reframed (a3 criticism 10; a2 caveat) |
| M-15 | P2 | Medium | After Task 2 both codebase tiers in the routing ref say "writes no nested directory" and the ref never names `/sc:analyze` (Tier 1 is auggie only), while Wave 2A loads only that ref section. A reader of the ref concludes codebase enrichment never nests. | Task 2's bullet text is the one in "Replacement wording" (it names `/sc:analyze` as the only writer of `nested/analyze-<n>/`). | routing:9-33; SKILL:179,187,195 | INV-016 |
| M-16 | P2 | Medium | The plan claims future live plans will see the fix, but it forbids commits (plan:24) and 7.2 builds each live-check worktree from a committed branch (spec:282). Until the owner commits and merges these edits, a P2 author on another branch sees neither the spec sentence nor the new skill text. | Add one line to Constraints: "The edits reach the next live plan only after the owner commits and merges them; this plan does not commit." | plan:23-24; spec:282 | INV-002 |
| M-17 | P2 | Low | spec:443 (open item 8) says each phase's plan must resolve how the plugin command copies are kept in step before editing; plan:21 decides "not edited by this plan" but does not say it resolves item 8 for this change. | Add to plan:21: "This is this plan's resolution of spec open item 8 for `brainstorm.md`." | spec:443; plan:21 | V1 R1-8 (not a scored point) |
| M-18 | OPEN | High | INV-020: from P2, brainstorm's research enrichment passes `--unattended` and a nested report directory (spec:142, spec:222); research-deep `fallback_1` is itself a nested command (`Skill sc:research-protocol`, routing:69), and the deep final fallback inherits the tier (routing:73). The corrected live-check sentence covers only the codebase wave. | No change in this plan (outside the brief, which covers the codebase wave). Pass to the user and to the P2 live-plan author as an open conflict. Not resolved. | spec:142,222; routing:42-73 | Invariant probe, HIGH, blocking |

Withdrawn or replaced card claims (do not appear in the merged card): V1 R1-1's "Task 1's first clause is vacuous" (X-001); V1 R1-5's "say an auggie scan (tier primary)" remedy (a1 New evidence (a)); V2 R2-1's "doubly" (X-005); V2 R2-7's fixed 18 (INV-008); V3 R3-1's `source`-field remedy (SKILL:372); V3 R3-2's P1 (now M-06 at P2); V3 R3-8 (withdrawn, a3 criticism 5); V3 R3-5's "wrong spot" (now the M-07 split). The Tier-1 card's F-1 is superseded by M-02, F-2 by M-09, F-4 by M-10; F-3 (lint-architecture baseline) stays as an unverified note covered by Task 7's `make lint`.

## Replacement wording

This section resolves the open C-007/X-003 design question (`debate-transcript.md:675,717`).

### Facts verified for this section

| Fact | Where (Read for this plan) |
|---|---|
| The codebase row offers `/sc:analyze` OR `mcp__auggie__codebase-retrieval`; its trigger is `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase`, or `--codebase` forced | SKILL:187-188 |
| Under `--unattended` only the two research rows are skipped; the codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/`; "The nested contract is listed in `artifacts`." | SKILL:195 |
| `primary` = "first-choice source ran cleanly"; `fallback_1` = "primary failed, used codegraph and native Glob/Grep"; `skipped` = "enrichment not invoked"; recorded as `enrichment_used: [{source, quality_tier}]` | SKILL:197-201 |
| `source` takes only `codebase \| research-light \| research-deep`; the contract also carries `domain` | SKILL:367,371-373 |
| Routing Tier 1 (primary) is auggie only; Tier 2 (fallback_1) activates "if Tier 1 returns error OR empty result"; nothing defines a step from a failed `/sc:analyze` to `fallback_1` | routing:16-31 |
| Per-source timeout 120 s (configurable); on timeout the source is recorded `skipped` | routing:77 |
| Command file: the analyze enrichment receives the nested `--report-dir`; "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`"; `<n>` is never reused | cmd:157 |
| WC-4: the contract is written "on success, failure, blocked and partial outcomes, including stops before any other output exists" | spec:72 |
| `/sc:analyze` writes its contract "on every outcome", and refuses an unusable report directory in chat only | `src/superclaude/commands/analyze.md:97-98` |
| 7.2 step 5: top-level session file plus subagent files under `subagents/`; tool calls are `tool_use` blocks with a `name`; a missing or ambiguous file makes conditions `not verifiable` and the phase not PASS without the owner's written acceptance | spec:292,300,302 |

### Faults each earlier proposal carried, and how the sentence below avoids them

| Proposal | Fault | Probe row | Avoided by |
|---|---|---|---|
| plan:81 (and src:9's sketch) | Ties the folder to `primary` / `fallback_1` | C-007, X-003 | The sentence never maps a tier to the folder and states that the tier fields do not record it |
| a1:52 (V1 session-file sentence) | Clause overlap: a failed analyze followed by codegraph fires both "folder exists" and "no folder expected" | a2:34 caveat 1 | No clause says "no folder" for any tool or tier |
| a1:52, a3:69 | Reads the top-level session file only, or by tool name `sc:analyze`, which `analyze.md` never names | INV-024 | Detects the call by its argument (`--report-dir <report directory>/nested/analyze-<n>/` with a number for `<n>`), in the top-level and subagent files, in `Skill`, `Agent` or `Task` calls, so an inline run through a Task prompt is also seen |
| a3:69 | Drops the P1 extra's "a wave that did not run is recorded as not run" guard | INV-007 | First clause requires a `source: codebase` entry whenever the codebase row applied (from `--codebase`, or from the contract's own `domain`) |
| a3:69 | "Every `nested/analyze-<n>/` holds its own `return-contract.yaml`" falsely fails a run whose analyze call was cut off by the timeout | INV-012 | Only directories that hold a contract must be listed; the required-folder clause is lifted when the `codebase` entry is `skipped` |
| a3:69, a3 Task 1-3 rule | Asserts that a failed `/sc:analyze` falls back to `fallback_1`, which no product text defines | INV-011 | No tier is stated for any `/sc:analyze` outcome |
| a1 consequence 1 | Pins `session file`, which the spec already holds many times | INV-017(a) | AC pins phrases unique to the new sentence (M-07) |

### Task 6 live-check sentence (replaces the second sentence of plan:81; written into spec 7.2 step 4 per M-07)

> A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`, and every `nested/analyze-<n>/` directory that holds a `return-contract.yaml` is listed in `artifacts`; such a directory is required only when a `Skill`, `Agent` or `Task` tool call in the worker's session file or in one of its subagent files (7.2 step 5) passes `--report-dir <report directory>/nested/analyze-<n>/` with a number for `<n>`, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).

Companion first sentence (replaces the first sentence of plan:81; stays in the 2.1 bullet, spec:62):

> A nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran, a run that failed included; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan through `mcp__auggie__codebase-retrieval`, or through codegraph, then Glob and Grep) writes no nested directory and records the tier it used in its own contract, and brainstorm's live-check extra for this is in 7.2 step 4.

Check against lc10: `--codebase` was passed and `enrichment_used` held a `codebase` entry on `fallback_1`; no `/sc:analyze` call was made (lc10-result.md, step 5 note); no nested analyze folder existed or was listed. Every clause holds, so lc10 passes the corrected extra, which is the owner's decision (`p1-owner-decisions-20261105.md:9`).

No single sentence survives the probe with zero residual risk. This is the sentence with the smallest remaining risk: it has no known false FAIL on a correct run. Its exact residual risks, all in the false-PASS direction:
1. A `/sc:analyze` call made without the nested `--report-dir` (a broken propagation, itself a defect) is not seen, so its missing folder passes. Related: INV-022 (no live check can force the analyze route).
2. The call names `Skill`, `Agent` and `Task` are INFERRED from Claude Code's session format (spec:302 says only "`tool_use` blocks with a `name`"); a call through another tool name is missed and its missing folder passes.
3. The `skipped` carve-out also exempts an invoked `/sc:analyze` that wrote nothing and was recorded `skipped` for a reason other than the timeout.
4. The required-folder clause depends on the session file; when it is missing or ambiguous the clause is `not verifiable`, and spec:300 then blocks a PASS until the owner accepts the gap in writing (accepted by design, INV-023).

### Wording rule for Tasks 1-3

> **Rule:** every "no nested directory" statement names its writer (the `mcp__auggie__codebase-retrieval` scan, the `fallback_1` tier of codegraph then native Glob and Grep), never a recorded `quality_tier` or a run; it says that `nested/analyze-<n>/` is written only by a `/sc:analyze` call and that `enrichment_used` does not show whether that directory exists; it states no tier for any `/sc:analyze` outcome and no step from a failed `/sc:analyze` to `fallback_1`; it uses the shared phrase `no nested directory and no nested contract`; and it keeps the nested contract listed in `artifacts` unconditionally, a failed call's included, never "only for a command that ran".

Applied text (exact; the merge executor copies these into the merged card's M-03 remedy):

- **Task 1** (SKILL:195): replace everything after "(`<n>` starts at 1)" with: "; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed." Task 1 AC: the paragraph contains `fallback_1`, `write no nested directory`, `nested/analyze-`, `skipped` and `` only by a `/sc:analyze` call ``; one line replaced.
- **Task 2** (routing): add one bullet as the last bullet of each codebase tier list (after routing:22 and after routing:31): "- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`." `grep -c 'writes no nested directory'` still prints 2; two lines added, none deleted.
- **Task 3** (cmd:157): append to the `**Nested invocations.**` bullet: "A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists." Leave "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" unchanged.
- **Task 4 pins**: in the paragraph slice (M-04): `fallback_1`, `write no nested directory and no nested contract`, `` only by a `/sc:analyze` call ``, and `Quality-tier tracking` absent; in each routing tier slice (M-05): `writes no nested directory and no nested contract` and `` only by a `/sc:analyze` call ``.
- **Task 5 pins**: add `writes no nested directory and no nested contract` and `` only by a `/sc:analyze` call `` to `UNATTENDED_EXPECT["brainstorm"]["phrases"]` (two new removed-token cases, M-08).

Checks of the applied text: no `src/superclaude/` path and no Orca command (plan:22); none of the `_FORBIDDEN` tokens (`test_brainstorm_protocol.py:15-21`); `skipped` and `nested/analyze-` stay in the SKILL paragraph; `nested/analyze-` and `nested/adversarial-` stay in the command bullet; the Tier 2 bullet stays inside the `test_codegraph_adoption.py:75-82` slice. The research wording is not touched (INV-020 stays open).

## Invariant probe disposition

| INV | Severity | Disposition |
|---|---|---|
| INV-001 | MEDIUM | Addressed by M-02: the before snapshot is taken in Task 1 before any edit, and the package's own path is exempt, which covers the `??` to `A` flip from `git add .dev/tasks`. |
| INV-002 | MEDIUM | Addressed by M-16 (Constraints line: the edits reach the next live plan only after the owner commits and merges them). |
| INV-005 | LOW | Addressed by M-04 (`Quality-tier tracking` must be absent from the paragraph slice, so a slicer that returns the whole section fails). |
| INV-006 | LOW | Not being made. `_check_unattended_section` is shared by every command's section test; scoping it to one bullet is a helper change outside the brief. The new pin `` only by a `/sc:analyze` call `` occurs only in the Nested invocations bullet today, which lowers the residual. |
| INV-007 | MEDIUM | Addressed by the live-check sentence's first clause (a `source: codebase` entry is required whenever the codebase row applied). |
| INV-008 | LOW | Addressed by M-08 (before-count plus the number of phrases added; no hard-coded 18 or 19). |
| INV-011 | MEDIUM | Addressed by the Tasks 1-3 rule and the live-check sentence: no tier is stated for any `/sc:analyze` outcome. |
| INV-012 | MEDIUM | Addressed by the live-check sentence: only directories holding a contract must be listed, and the required-folder clause is lifted when the `codebase` entry is `skipped`. Residual 3 above remains. |
| INV-016 | MEDIUM | Addressed by M-15 (the routing bullets name `/sc:analyze` as the only writer of `nested/analyze-<n>/`). |
| INV-017 | MEDIUM | Addressed by M-07: Task 6's AC is rewritten for two changed lines, and its pins are phrases unique to each new sentence instead of `session file`. |
| INV-020 | HIGH | OPEN CONFLICT, not resolved. Outside this plan's brief (src:1-9 cover the codebase-enrichment wave). Passed to the user and the P2 live-plan author: from P2 the research enrichment passes `--unattended` and a nested report directory (spec:142, spec:222), research-deep `fallback_1` is itself a nested command (routing:69) and the deep final fallback inherits the tier (routing:73), so the P2 plan needs its own research-wave live-check wording. The Tasks 1-3 text names the codebase `fallback_1` tier explicitly (codegraph, then Glob and Grep), which reduces but does not remove the risk that a reader applies it to research. Convergence stays BLOCKED_BY_INVARIANTS until the owner accepts this as a risk or a P2 plan addresses it. |
| INV-021 | MEDIUM | Addressed by M-07: the live-check sentence goes into 7.2 step 4, which every live plan follows, with a pointer from the 2.1 bullet. |
| INV-022 | MEDIUM | Not being made. No flag forces `/sc:analyze` (SKILL:187 lets the worker choose), and adding one changes the skill's routing, which the brief does not ask for. Residual: no live check proves the nested analyze route works; pass to the owner with INV-020. |
| INV-024 | LOW | Addressed by the live-check sentence: the call is detected by its nested `--report-dir` argument in top-level and subagent files, not by a tool name. Residual 2 above remains. |

## Changes NOT Being Made (with rationale)

| Diff point / item | Non-base approach | Rationale for not taking it |
|---|---|---|
| C-007 / X-003 remedy | V3: decide by the `source` field of `enrichment_used` | `source` holds only `codebase \| research-light \| research-deep` (SKILL:372); conceded by V3 (a3 criticism 1). |
| C-007 remedy | V1 card: say "an auggie scan (tier primary)" | Fixes the `primary` half only; the `fallback_1` half stays false (a3 criticism 12). |
| C-007 remedy | V1 Round 2 session-file sentence (a1:52) as written | Clause overlap in the failed-analyze case (a2 caveat 1); top-level-only reading (INV-024). |
| C-007 remedy | V3 Round 2 folder-plus-session-file sentence (a3:69) as written | INV-007, INV-011, INV-012, INV-024. |
| Tasks 1-3 wording | V3 rule "also when it failed and the scan fell back to `fallback_1`" | Undefined tier step (INV-011). |
| Task 6 pin | V1/V2: add `session file` to Task 6's pinned phrases | Not unique in the spec (INV-017(a)). |
| Task 6 placement | Literal src:9 second branch, a note in the P1 rows of 7.3 (AC-1.2) | Later live-plan authors read 7.2, not the P1 rows (INV-021); the debate allowed either (a1:58, a3:73). |
| `enrichment_used` | Add a tool field to the contract | Changes the stable contract (SKILL:360-377); owner's decision (a1 consequence 3, a2 caveat 2). |
| src:9 sketch | Copy it verbatim | Falsified by the analyze-clean and analyze-failed cases (a2 New evidence 2). |
| C-003 / X-002 | V3: P1 | All three agree P2 (a3 criticism 4). |
| C-013 | V3 R3-8 | Withdrawn as a misreading of plan:21 (a3 criticism 5). |
| X-005 | V2: "doubly unpassable" | Second clause is reading-dependent (a2 criticism 3). |
| C-008 | V2: fixed post-edit count 18 | Depends on the number of phrases added and on the tree state (INV-008, A-004). |
| X-001 | V1: Task 1's first clause is vacuous | False (SKILL:195 lacks `fallback_1`; a1 criticism 1). |
| F-3 | V1: partly disputes the lint-architecture note | Not debated; Task 7's `make lint` runs `lint-architecture`, so no plan change is needed. |
| INV-006 | Bullet-scoped command-file check | Shared helper change outside the brief (see disposition). |
| INV-022 | Force the analyze route in a live check | No such flag; skill routing change outside the brief. |
| INV-020 | Research-wave wording | Outside the brief; open conflict for the owner and the P2 author. |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|---|---|---|---|
| 1 | Medium | The new live-check sentence misjudges a run shape not in the probe; residuals 1-4 are false PASSes | Revert M-01's remedy to "replacement wording not agreed" and pass C-007 to the owner |
| 2 | Low | A wrongly written status diff blocks Task 7 again | Revert to base R2-1 text with V1's remedy only |
| 3 | Low | A paragraph slicer that misses the paragraph fails Task 4 loudly | Use the section slice plus the INV-005 absence check |
| 4 | Low | Tier slices mis-bounded | Keep the `grep -c` smoke check alone |
| 5 | Medium | Two-line spec diff conflicts with another edit to spec:286 | Put both sentences back in the 2.1 bullet and restore the one-line AC |
| 6 | Low | Shared phrase misspelled between task and pin | Pins are copied from the applied text above, byte for byte |
| 7-11 | Low | Additive wording fixes | Remove the added finding |
| 12 | Low | Additive | Remove the added finding |

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-06T01:24:00Z
- Review status: auto-approved
