# Refactoring Plan: Merge into Base (Variant 1)

## Overview

- Base: Variant 1 (reviewer-1 card, analyzer, sonnet), combined score 0.829 (`base-selection.md`).
- Incorporating strengths from: Variant 3 (refactorer, opus), Variant 2 (qa, haiku slot), plus orchestrator findings taken from `invariant-probe.md` (no card found them).
- Merged output: one consolidated verdict card on the plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md` ("plan") against its brief `source.md` in the same folder ("brief").
- Planned changes: 14 (12 incorporations, 1 orchestrator insertion group, 1 base-internal correction group).
- Final finding list: 16 findings (1 P1, 4 P2, 11 P3) plus 5 confirmations. The P1 and the four P2 all sit in brief Part 4 and the Task 6 lines that copy it.
- Risk level: Medium overall (M-01 is a P1 that rests on an INFERRED failure; see its rationale).
- Verified on disk while writing this plan: `SKILL.md:183,187,195,388`; `analyze.md:2,97-98`; `handoff-routing.md:77`; `WORKER-CONTRACT.md:32`; spec lines 62, 282-302; `brainstorm.md:153-157`; `lc10-result.md:13`; `pyproject.toml:50-54`; `sc-implement-protocol/SKILL.md:97`; plan lines 25, 44, 95, 111, 125, 128, 131, 133-137, 142-144, 152-157; brief lines 45, 109, 111, 199, 201, 217, 225, 229, 237-241; `git --no-optional-locks status --porcelain -- .dev/tasks/to-do` (earlier package `...001016` is `A`, this package `...021737` is `??`).

## Consolidated verdict (for the merged card's header)

Not ready for `/sc:implement` until the owner amends brief Part 4 as in "Recommended wording fix" and the plan mirrors it (plan:128, plan:135-137 plus one new bullet, plan:143). Everything else in the plan is executable as written; the P3 items are optional hardening and owner notes. The plan copies Part 4 faithfully (confirmed by all three cards), so the defect is brief-owned. Suggested card confidence: 0.72 (mean blind-calibrated 0.737, lowered because M-01 is INFERRED).

## Planned Changes

### Change 1: C-001 evidence and tag (from Variant 3)
- **Source**: V3 R3-1 (evidence `analyze.md:97-98`, `WORKER-CONTRACT.md:32`, `SKILL.md:388`; claim that plan:133 "no known false FAIL" is false as written).
- **Target**: Base A-2 (replace evidence list and tag; becomes M-02).
- **Rationale**: Round 2, C-001 won by V3 at 80% (A1, A2 on evidence; A3 split crediting V1 for severity and fix shape); X-001 V3 at 92%; A-001 QUALIFY 95%. All three advocates set it at P2 and brief-owned.
- **Integration**: Keep V1's P2 and its timeout trigger. Tag becomes "Grounded conflict, INFERRED failure" (R2-A1 row 1, R2-A3 row 2). Drop V3's remedy (withdrawn, R2-A3 row 3).
- **Risk**: Low. Evidence-only replacement.

### Change 2: INV-019 as the card's P1 (orchestrator insertion, from the invariant probe)
- **Source**: `invariant-probe.md` INV-019 (Round 2.5, sufficiency_challenge, HIGH, UNADDRESSED). No card raised it.
- **Target**: New M-01 at the top of the finding list.
- **Rationale**: The convergence gate blocked on it (`debate-transcript.md`, Convergence Assessment). See M-01 for the P1 decision.
- **Integration**: Insert as orchestrator-sourced, tagged INFERRED, with the fix pointing at "Recommended wording fix".
- **Risk**: Medium. The failure path has not been observed (`lc10-result.md:13` lists Skill calls only).

### Change 3: Recommended Part 4 wording fix (from the Round 2 rebuttals and the probe)
- **Source**: V1 advocate "Proposed wording fix" (R2, carve-outs moved forward); V2 advocate R2 (a) ("Mostly yes"; needs the owner to amend Part 4 first, F-1 byte-for-byte verifier brief:45); V3 advocate R2 "Recommended resolution of C-001" (option (a), owner amends Part 4; Edits 2-3); probe INV-011, INV-012, INV-015, INV-019.
- **Target**: New card section "Recommended wording fix" (text below), referenced by M-01 to M-05.
- **Rationale**: All three advocates agreed in Round 2 that the fix belongs in brief Part 4, not in the plan alone (V3 R2 rejects option (b) as the resolution because the P2 author reads only the spec). INV-015 (ADDRESSED) fixes the order: owner amends brief first, plan mirrors.
- **Integration**: The recommendation restructures the sentence instead of adding V1's parenthesis: the "listed entries exist" check moves inside the required-directory clause, so the skipped, refused and tool-error cases are exempt by construction and V3's Edit 2 is no longer needed.
- **Risk**: Medium. New wording that no reviewer has debated; checked below against every probe row it touches.

### Change 4: Residual-risk list (from Variant 3 and the probe)
- **Source**: V3 R3-6 (spec:60,62 already name the Skill and Agent tools); probe INV-013.
- **Target**: New M-04.
- **Rationale**: C-010 won by V3 at 92% (brief-owned, brief:239). INV-013 LOW, false-PASS only.
- **Integration**: Risk 2 is rewritten for the Skill-only trigger, which also absorbs C-010; risk 3 gains the one-entry sentence; a fifth risk records the unchecked listed entries of a non-required directory.
- **Risk**: Low.

### Change 5: Task 6 acceptance pin (from the probe)
- **Source**: `invariant-probe.md` INV-005 (MEDIUM); V2 advocate R2 (a) point 3 ("no AC checks byte for byte"); V3 advocate R2 "Known gap".
- **Target**: New M-05.
- **Rationale**: Without a pin unique to the amended sentence, a plan that keeps the old sentence passes every Task 6 AC.
- **Integration**: One pin, `` invokes `sc:analyze` ``, added to brief F-7's pin list (brief:109) and plan:143.
- **Risk**: Low. The pin occurs once in the amended sentence and nowhere in the old one.

### Change 6: F-16 Constraints line (from Variant 2)
- **Source**: V2 R2-1.
- **Target**: Replaces base dispute 4 ("plan's wording is the correct one", conceded overstated in R2-A1 row 5); becomes M-07.
- **Rationale**: C-002 split at 50% and X-003 split at 50% (V2 right on recording, V1 right on severity); A-002 QUALIFY 95% (a Constraints line cannot block `/sc:implement`, `qa.md:318`); A-005 QUALIFY 93%.
- **Integration**: P3, not P1. Fix with the brief's literal line.
- **Risk**: Low.

### Change 7: F-13 sentence (from Variant 2, merged with base A-4)
- **Source**: V2 R2-2 (necessary deviation forced by F-2, unrecorded).
- **Target**: Base A-4 (merge); becomes M-08.
- **Rationale**: C-003 V2 at 85% (A2 credits V1 for the sync-dev "only" point); X-004 V2 at 93%. The "only" flaw is brief-owned (brief:169).
- **Integration**: Keep V1's sync-dev point and V2's classification in one finding at P3.
- **Risk**: Low.

### Change 8: `--report-dir` contract split (from Variant 3)
- **Source**: V3 R3-3.
- **Target**: New M-12 (owner note).
- **Rationale**: C-007 split at 50% (V3 found it; V1 set P3 because conforming briefs pass `--output`, spec:142, `WORKER-CONTRACT.md:192`, `brainstorm.md:154`); INV-014 ADDRESSED at LOW.
- **Integration**: Note only, no plan change.
- **Risk**: Low.

### Change 9: Companion sentence vs installed twin (from Variant 3)
- **Source**: V3 R3-4.
- **Target**: New M-13 (owner note).
- **Rationale**: C-008 V3 at 90%; a fix needs a seventh file (plan:21); V3 R2 New evidence 3: spec:62 and `WORKER-CONTRACT.md:24` already differ.
- **Integration**: Note only.
- **Risk**: Low.

### Change 10: Routing bullet tier wording (from Variant 3)
- **Source**: V3 R3-5.
- **Target**: New M-14 (owner note).
- **Rationale**: C-009 V3 at 92%; `handoff-routing.md:77` records `skipped` on timeout; text is brief:230.
- **Integration**: Note only (changing it would break the Task 1-3 byte-for-byte rule of F-3).
- **Risk**: Low.

### Change 11: Coverage-matrix gap (from Variant 2)
- **Source**: V2 R2-5.
- **Target**: New M-15 (review-artifact note).
- **Rationale**: C-012 V2 at 90%; the plan satisfies the unsampled spans.
- **Integration**: Note only.
- **Risk**: Low.

### Change 12: Part 4 byte-for-byte confirmation (from Variant 3)
- **Source**: V3 R3-8.
- **Target**: Base A-7 (merge into confirmations OK-3).
- **Rationale**: C-014 none-winner at 97% (all three confirm).
- **Integration**: One confirmation line listing plan:38,54,69,122,128 = brief:229,230,231,221,217.
- **Risk**: Low.

### Change 13: Further probe rows (orchestrator insertion)
- **Source**: `invariant-probe.md` INV-002 (LOW), INV-020 (MEDIUM).
- **Target**: New M-11 (plan AC guard) and M-16 (owner note).
- **Rationale**: Both UNADDRESSED; see "Invariant probe disposition".
- **Integration**: M-11 is one AC clause; M-16 is a note.
- **Risk**: Low.

### Change 14: Base-internal corrections (Variant 1)
- **Source**: V1's own Round 2 concessions.
- **Target**: Base A-1, A-3, A-5, A-6, dispute 4.
- **Rationale**: A-1 Task 5 half withdrawn (R2-A1 row 6; C-005 V1 at 94%, narrowed); A-3 exit-code part dropped, format-check part kept (R2-A1 row 9; C-006 at 90%); A-5 is a confirmation, not a defect (C-004 at 97%, X-005 at 78%); A-6 to P3 cosmetic (C-013 none at 70%); dispute 4 removed (R2-A1 row 5). A-5's evidence "index check" is replaced by the command `git --no-optional-locks status --porcelain -- .dev/tasks/to-do`, re-run while writing this plan.
- **Integration**: A-1 becomes M-06 (P3), A-3 becomes M-09 (P3), A-5 becomes OK-1, A-6 becomes M-10 (P3).
- **Risk**: Low.

## Base weaknesses and the better variant

| Base weakness (V1) | Better variant | What the merged card takes |
|---|---|---|
| A-2 tagged the text conflict INFERRED although `analyze.md:97-98` was on disk | V3 R3-1 | Grounded evidence, split tag (Change 1) |
| A-2 proposed no fix | V1 and V3 advocates (Round 2) plus the probe | Recommended wording fix (Change 3) |
| Missed the `--report-dir` contract split | V3 R3-3 | M-12 |
| Missed the three brief-owned notes | V3 R3-4, R3-5, R3-6 | M-13, M-14, M-04 |
| Called the plan's F-16 wording "the correct one"; weak on recording discipline | V2 R2-1, R2-2 | M-07, M-08 |
| Did not check the review's own coverage matrix | V2 R2-5 | M-15 |
| A-1 Task 5 half factually wrong | none (V1 withdrew it) | Narrowed M-06 |
| A-3 bundled two defects | none (split by the debate) | M-09 keeps the format check only |
| A-5 cites an unreproducible "index check" | none | Replaced by the explicit command (Change 14) |
| Missed INV-019, INV-011, INV-005 | none of the cards; invariant probe | M-01, M-03, M-05 |

## Final consolidated finding list

Priority scale: P1 = fix before `/sc:implement`; P2 = should be fixed with the P1 (same edit); P3 = optional hardening or owner note. Each "Source" names the card finding and the debate resolution. "Brief" edits are owner amendments; this review edits neither the brief nor the plan.

### M-01 (P1, INFERRED, orchestrator from INV-019): the required-directory trigger keys on any Skill, Agent or Task call that passes the flag text
- **Claim**: brief:217 = plan:128 requires `nested/analyze-<n>/` when "a `Skill`, `Agent` or `Task` tool call ... passes `--report-dir <report directory>/nested/analyze-<n>/`". Wave 2A runs every enrichment source "in parallel via `Task` agents" (`SKILL.md:183`), the codebase row offers "`/sc:analyze` ... OR `mcp__auggie__codebase-retrieval`" (`SKILL.md:187`), and the same paragraph gives the nested `--report-dir` (`SKILL.md:195`). A worker that writes that command line into a Task prompt, whose subagent then takes the auggie or `fallback_1` path (the lc10 path, `lc10-result.md:8`), makes the sentence require a folder no one creates. That is the lc10 false FAIL again, and plan:133's "no known false FAIL" is false.
- **Why P1**: the debate set C-001 at P2 because it needs a timeout or refusal before the nested call writes. INV-019 needs only the ordinary delegation that `SKILL.md:183` prescribes plus the lc10 condition (auggie unavailable). It reproduces the exact failure the plan exists to remove (brief Part 1 background; plan:19). Once Task 6 runs, the spec carries the sentence, and fixing it later needs a second spec edit while F-1's byte-for-byte verifier (brief:45) points at stale text (V3 advocate R2). It cannot block `/sc:implement` (no AC reads it), so it is P1 by decision, not by an executor gate. Failure tag INFERRED: no session record shows a Task prompt carrying the flag.
- **File**: brief:217 (owner), then plan:128.
- **Exact change**: replace the quoted live-check sentence with the amended sentence in "Recommended wording fix"; plan:128 then carries it byte for byte.
- **Verifier**: brief:217 and plan:128 each contain `` a `Skill` tool call (not a `Task` or `Agent` call `` and `` invokes `sc:analyze` ``, and neither contains `` a `Skill`, `Agent` or `Task` tool call ``; the quoted sentence at plan:128 equals the one at brief:217 byte for byte.

### M-02 (P2, Grounded conflict, INFERRED failure; V1 A-2 + V3 R3-1): the "listed paths exist" clause has no carve-out
- **Claim**: Task 1's tail "The nested contract is listed in `artifacts`, also when the call failed." (plan:38 = brief:229) and the live-check clause "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" (plan:128 = brief:217) conflict for a call that timed out before writing (`handoff-routing.md:77`) or whose directory `/sc:analyze` refused ("printed in chat only", `analyze.md:97`). The carve-outs sit only on the later "required only when" clause.
- **File**: brief:217 (owner), then plan:128. Task 1 tail (brief:229, plan:38) unchanged.
- **Exact change**: the amended sentence moves the existence check inside the required-directory clause ("and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing"), so skipped, refused and tool-error calls are exempt by construction.
- **Verifier**: plan:128 no longer contains `every `nested/analyze-` path listed in `artifacts` exists`; it contains `must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing`; plan:38 and the Task 1 AC (plan:45) unchanged.

### M-03 (P2, Grounded, orchestrator from INV-011): file entries checked as directories
- **Claim**: `artifacts` lists files ("every other file written", `WORKER-CONTRACT.md:32`; "the nested contracts", `SKILL.md:388`), but plan:128 tests a listed path with a directory predicate ("exists and holds its own `return-contract.yaml`") and asks that a directory be "listed in `artifacts`". A literal checker tests `<listed file>/return-contract.yaml` and fails a correct run.
- **File**: brief:217 (owner), then plan:128.
- **Exact change**: in the amended sentence the listing rule names the file (`` every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts` ``) and the existence rule speaks of "the directory ... and every `artifacts` entry under it".
- **Verifier**: plan:128 contains `` every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts` `` and no longer contains `` directory that holds a `return-contract.yaml` is listed in `artifacts` ``.

### M-04 (P2; V3 R3-6 + INV-013 + the new wording): the residual-risk list must match the amended sentence
- **Claim**: plan:133-137 copy brief:237-241. Under the amended sentence, risk 2 is wrong (the trigger is now the Skill tool only, and spec:62 already names the Skill and Agent tools; only the session-file encoding is inferred), risk 3 misses INV-013 (one `codebase` entry exempts every call), and a new false-PASS risk exists (listed entries of a non-required directory are not checked). plan:133's lead-in ("all are in the false-PASS direction, and the sentence has no known false FAIL on a correct run") becomes true and stays.
- **File**: brief:239, brief:240, new line after brief:241 (owner); plan:135, plan:136, new bullet after plan:137.
- **Exact change**: the texts in "Recommended wording fix", part C.
- **Verifier**: plan:135 contains `sees only a `Skill` tool call that invokes `sc:analyze``; plan:136 contains `it exempts every `nested/analyze-<n>/` call of the run at once`; the residual-risk list has five bullets; plan:133 unchanged.

### M-05 (P2, Grounded, orchestrator from INV-005): no Task 6 AC tells the amended sentence from the old one
- **Claim**: plan:143 pins `lc10`, ``a `source: codebase` entry`` and ``neither `quality_tier` nor `source` records``; all three are in both the old and the amended sentence, so a plan that keeps the old text passes Task 6.
- **File**: brief:109 (F-7's pin list; owner), plan:143. Brief:111 ("its AC lists exactly these pins") needs no edit once :109 names the new pin.
- **Exact change**: brief:109: replace "the 7.2 step 4 line contains `lc10`, `` a `source: codebase` entry `` and `` neither `quality_tier` nor `source` records ``;" with "the 7.2 step 4 line contains `lc10`, `` a `source: codebase` entry ``, `` neither `quality_tier` nor `source` records `` and `` invokes `sc:analyze` ``;". plan:143 becomes: "- The section 7.2 step 4 line contains `lc10`, ``a `source: codebase` entry``, ``neither `quality_tier` nor `source` records`` and ``invokes `sc:analyze` ``."
- **Verifier**: plan:143 contains `invokes `sc:analyze``; `grep -c 'invokes `sc:analyze`'` on the amended sentence prints 1 and on the current plan:128 prints 0.

### M-06 (P3, Grounded; V1 A-1 narrowed): Task 4's routing-ref `git show` can pass on a wrong path
- **File**: plan:95.
- **Exact change**: replace "and the same command for `refs/handoff-routing.md` with `writes no nested directory and no nested contract` both print 0" with "and `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md | grep -c 'writes no nested directory and no nested contract'` both print 0, and `git cat-file -e HEAD:<path>` exits 0 for both paths".
- **Verifier**: plan:95 contains `HEAD:src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` and `git cat-file -e`.

### M-07 (P3, Grounded; V2 R2-1, severity per V1): F-16 Constraints line departs from the brief and is unrecorded
- **File**: plan:25.
- **Exact change**: replace the line with the brief's literal line: "- The edits reach the next live plan only after the owner commits and merges them; this plan does not commit." (brief:199; true under spec:282, which builds the live worktree from a committed branch).
- **Verifier**: plan Constraints contains that line exactly (F-16 verifier, brief:201).

### M-08 (P3, Grounded; V2 R2-2 + V1 A-4): F-13 sentence widened without a record, and "only" is untrue because of `make sync-dev`
- **File**: plan:152.
- **Exact change**: replace "Do not edit any source file in this task; it writes only the logs and the status snapshot under `./artifacts/`." with "Do not edit any source file in this task; it writes only the logs under `./artifacts/`. The status snapshot `./artifacts/status-after.txt` (correction F-2) is the one non-log file it writes there, and `make sync-dev` rewrites the gitignored copies under `.claude/` (output, not edits)."
- **Verifier**: plan:152 contains the F-13 sentence verbatim (brief:169-171) and names `status-after.txt` and `.claude/`.

### M-09 (P3, INFERRED; V1 A-3, format-check part only): Task 7 runs no format check on the two edited test files
- **File**: plan:152 and plan:156.
- **Exact change**: plan:152 adds "and `uv run ruff format --check tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py`" to the commands saved to `./artifacts/t7-lint.log`; plan:156 adds "and `ruff format --check` on the two edited test files exiting 0".
- **Verifier**: Task 7 body and its second AC both name `ruff format --check`.

### M-10 (P3, Grounded, cosmetic; V1 A-6 + V2 R2-4): Task 6 anchor omits the enumerator
- **File**: plan:125.
- **Exact change**: `begins "Check the contract (PyYAML is a declared dependency"` becomes `begins "4. Check the contract (PyYAML is a declared dependency"` (spec:286).
- **Verifier**: plan:125 contains `"4. Check the contract`.

### M-11 (P3, Grounded, orchestrator from INV-002): `status-before.txt` has no checkable pre-edit guard
- **File**: plan:44.
- **Exact change**: append ", and names none of the six files in Constraints" to the first Task 1 AC.
- **Verifier**: plan:44 contains `names none of the six files`.

### M-12 (P3 owner note; V3 R3-3): with `--report-dir`, `domain` and `enrichment_used` are in brainstorm's own contract
- **File**: none in the plan. Evidence: `brainstorm.md:153-154`, `SKILL.md:381`, spec:142.
- **Exact change**: card note only: the live-check sentence reads "the contract's `domain`", which is right for the `--output` briefs the spec requires; a brief that passes `--report-dir` must read the own contract listed in `artifacts`.
- **Verifier**: the card lists it under owner notes with this evidence.

### M-13 (P3 owner note; V3 R3-4): companion sentence states a rule for every command; the installed twin is not edited
- **File**: none (a fix needs a seventh file, plan:21). Evidence: plan:122, spec:62, `WORKER-CONTRACT.md:24`.
- **Exact change**: card note only.
- **Verifier**: listed under owner notes.

### M-14 (P3 owner note; V3 R3-5): routing bullet says the scan is recorded "with this tier's `quality_tier`", but a timeout records `skipped`
- **File**: none (brief:230 text; F-3 requires it byte for byte). Evidence: plan:54, `handoff-routing.md:77`.
- **Exact change**: card note only; the owner may amend brief:230 in the same Part 4 amendment (the tail is not pinned).
- **Verifier**: listed under owner notes.

### M-15 (P3 review-artifact note; V2 R2-5): the coverage matrix never sampled brief Part 2, the Part 3 preamble or Part 4
- **File**: `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/artifacts/coverage-matrix.yaml:9-36` (not edited). The plan satisfies those spans.
- **Exact change**: card note only.
- **Verifier**: listed under review notes.

### M-16 (P3 owner note, orchestrator from INV-020): the next live-plan author has no pointer to the new 7.2 step 4 sentence
- **File**: none in this plan (the archived P1 brief and plan are read-only, plan:19, and outside the six files). Evidence: `decisions/APPROVED.md:64`, archived `source.md:62`, `p1-owner-decisions-20261105.md:9`.
- **Exact change**: card note: the owner points the P2 brief author at spec 7.2 step 4 and does not copy the archived P1 brainstorm extra.
- **Verifier**: listed under owner notes.

### Confirmations (no change)
- **OK-1** (V1 A-5; C-004 97%, X-002 97%, X-005 78%): Task 7 bullet 3 holds on today's tree; `git --no-optional-locks status --porcelain -- .dev/tasks/to-do` shows `...001016` as `A` and only this package as `??`, which plan:157 exempts.
- **OK-2** (C-011 93%): Tasks 2, 3, 6 need no "Depends on: Task 1"; the executor runs "Default sequential in source order" (`sc-implement-protocol/SKILL.md:97`).
- **OK-3** (V1 A-7 + V3 R3-8; C-014 97%): pins, slices and the Part 4 copy hold: plan:38,54,69,122,128 equal brief:229,230,231,221,217; the paragraph slice ends at `SKILL.md:196`.
- **OK-4** (INV-007): `-k brainstorm` collects 17 today and 19 after Task 5.
- **OK-5** (INV-010, re-checked against the amended sentence): the lc10 replay (auggie unavailable, `fallback_1`, no Skill call to `sc:analyze`) passes; so does INV-019's falsifier (Task prompt carries the flag, subagent takes `fallback_1`).

## Recommended wording fix

An OWNER amendment of brief Part 4. The plan copies Part 4 byte for byte (F-1 verifier, brief:45), so the plan cannot take this text on its own; the order is: owner amends the brief, then the plan is regenerated or edited at the lines named in part D. The rule of brief:225 (nested contract listed in `artifacts` unconditionally, a failed call's included) is kept: Task 1's tail is not changed, and the check no longer fails a listed contract that a skipped, refused or tool-error call never wrote.

### A. Amended Task 6 live-check sentence (replaces brief:217; plan:128 then carries it)

```text
A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts`; a `nested/analyze-<n>/` directory is required, and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing, only when a `Skill` tool call (not a `Task` or `Agent` call whose prompt only names `/sc:analyze`) in the worker's session file or in one of its subagent files (7.2 step 5) invokes `sc:analyze` with `--report-dir <report directory>/nested/analyze-<n>/` and a number for `<n>` and returns no tool error, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).
```

What changed and why:
- **INV-019**: the trigger is an actual Skill call that invokes `sc:analyze`, not any Skill, Agent or Task call that passes the flag text. Task and Agent prompts that only mention the command no longer count. A Skill call that returns a tool error (the command never loaded) does not count either.
- **C-001**: the "listed entries exist" check now applies only to a required directory, so the timeout (`skipped`), refusal and tool-error cases are exempt by construction. A call with a usable directory that failed must still have written its contract (`analyze.md:98`), so its missing file is still a true FAIL.
- **INV-011**: the listing rule names the contract file, and the existence rule speaks of the directory and the `artifacts` entries under it.
- **Pins kept**: `lc10`, ``a `source: codebase` entry`` and ``neither `quality_tier` nor `source` records`` are still present (plan:143). It is still one appended line in step 4 (plan:144). No test reads the spec.
- **Not changed**: "the contract's `domain`" (M-12, P3); "this last clause ... `not verifiable`" still names the required-directory clause, so residual risk 4 needs no edit. V3's Edit 2 is no longer needed.

Why a Skill call is the right trigger, checked on disk: Wave 2A hands each source to a `Task` agent (`SKILL.md:183`), so a real `/sc:analyze` run appears as a Skill tool call in that subagent's file, which 7.2 step 5 already reads (spec:292: "each subagent's own file is under ... `subagents/`"). The spec's nested propagation rule names "the Skill tool or the Agent tool" (spec:62); an Agent-tool route still reaches `/sc:analyze` through a Skill call in the subagent file. lc10's record shows how Skill calls appear: by skill name (`sc:brainstorm-protocol`, `sc:adversarial-protocol`, `lc10-result.md:13`). A refusal is "printed in chat only" (`analyze.md:97`), so it can be judged only from the session file, which is what the required clause already reads.

Residual risk after the fix (all false-PASS, none false-FAIL):
- A `/sc:analyze` run not made through a Skill call (for example a subagent that reads the command file and follows it), or recorded under a skill name other than `sc:analyze` (the command's own name is `analyze`, `analyze.md:2`; the `sc:` form is inferred from lc10's other Skill names), is not seen, and its missing folder passes. The "every existing contract is listed" clause still catches an unlisted contract.
- How the session file records the Skill input (`skill`, `args`) and a tool error is INFERRED from Claude Code's session format (spec:302 says only "`tool_use` blocks with a `name`").
- Listed entries under a directory that is not required are not checked for existence. This is the case Task 1's "also when the call failed" produces, so it is intended.
- With the session file unverifiable the required clause is `not verifiable`, which blocks PASS until the owner accepts the gap (spec:300), unchanged.

### B. Task 1 skill tail (brief:229, plan:38)

No change. The tail "The nested contract is listed in `artifacts`, also when the call failed." stays byte for byte, as does its AC (plan:45). Rewording it (V3 R3-1's original remedy) breaks brief:225 and was withdrawn in Round 2.

### C. Residual-risk block (brief:237-241; plan:133-137)

- brief:237 and plan:133: no change. With part A the claim "no known false FAIL on a correct run" is true.
- brief:238 / plan:134 (risk 1): no change.
- brief:239 (risk 2) becomes: "2. The required-directory clause sees only a `Skill` tool call that invokes `sc:analyze`. The spec's nested propagation rule (spec:62) names the Skill tool, but how the session file records the invoked command, its arguments and a tool error is INFERRED from Claude Code's session format (spec:302 says only "`tool_use` blocks with a `name`"); a `/sc:analyze` run made another way, or recorded under another name, is missed and its missing folder passes."
- plan:135 becomes: "- The required-directory clause sees only a `Skill` tool call that invokes `sc:analyze`; the spec's nested propagation rule names the Skill tool, but how the session file records the invoked command, its arguments and a tool error is inferred from Claude Code's session format (the spec says only that the session file records `tool_use` blocks with a `name`); a `/sc:analyze` run made another way, or recorded under another name, is missed and its missing folder passes."
- brief:240 (risk 3) and plan:136 append: ", and, because `enrichment_used` holds one `codebase` entry, it exempts every `nested/analyze-<n>/` call of the run at once" before the closing period.
- brief:241 / plan:137 (risk 4): no change.
- New risk 5 after brief:241: "5. An `artifacts` entry under a directory that is not required (a `skipped`, refused or tool-error call) is not checked for existence; Task 1's "also when the call failed" produces exactly this case." The same text, as a bullet, goes after plan:137.

### D. Plan lines that must change after the owner amends the brief

| Plan line | Change | Finding |
|---|---|---|
| plan:128 | The part A sentence, byte for byte | M-01, M-02, M-03 |
| plan:133 | None (the claim becomes true) | M-04 |
| plan:135, plan:136, new bullet after plan:137 | Part C texts | M-04 |
| plan:143 | Add pin ``invokes `sc:analyze` `` (with brief:109) | M-05 |
| plan:131 | None (Necessary-deviation record still accurate) | n/a |
| plan:144 | None (still two lines changed) | n/a |

If the owner declines the amendment: plan:128 must stay as it is (F-1, brief:45). The plan then narrows plan:133 to "has two known false-FAIL paths" and adds two bullets naming them (INV-019's Task-prompt path; C-001's timeout or refusal path), recorded as a departure from brief:237 next to plan:131 (V2 advocate R2 option (b)). INV-019 then stays open.

## Invariant probe disposition

| INV | Severity | Disposition | Status |
|---|---|---|---|
| INV-002 | LOW | M-11 (status-before guard AC at plan:44) | Addressed in the recommendation; open in the plan until plan:44 is edited |
| INV-005 | MEDIUM | M-05 (pin ``invokes `sc:analyze` `` in brief:109 and plan:143) | Addressed in the recommendation; open in the plan until the owner amends brief:109 and plan:143 mirrors it |
| INV-011 | MEDIUM | M-03, part A (file-typed listing rule, directory-typed existence rule) | Addressed in the recommendation; open in the plan until the owner amends Part 4 |
| INV-013 | LOW | M-04, part C risk 3 (recorded, not removed; false-PASS only) | Addressed in the recommendation as a recorded risk; open in the plan until plan:136 is edited |
| INV-017 | LOW | Not being made. brief:225 binds only Tasks 1-3, which state both halves of the owner rule. The spec check does not need the contract half: the auggie and `fallback_1` scans write no contract, and "every existing contract is listed" covers what exists. Owner may add it later. | Accepted, open |
| INV-019 | HIGH | M-01, part A (Skill call that invokes `sc:analyze`, no tool error) | **Addressed IN THE RECOMMENDATION. Still OPEN in the plan** until the owner amends brief Part 4 and plan:128 mirrors it. Not resolved in the plan. |
| INV-020 | MEDIUM | Not being made in this plan: the fix touches the archived P1 package and decisions, which are read-only (plan:19) and outside the six files (plan:21). M-16 owner note. | Open (owner) |
| INV-021 | MEDIUM | Not being made: brief Part 5 (brief:245) orders no change for the research wave; plan:26 already records it as an open conflict. | Accepted, open (owner and P2 author) |

## Changes NOT Being Made (with rationale)

| Diff point / item | Non-base approach | Rationale for not taking it |
|---|---|---|
| C-001 / R3-1 remedy | V3: reword Task 1's tail to "listed when it was written" | Breaks brief:225 and the Task 1 AC (plan:45); withdrawn by V3 (R2-A3 row 3) |
| C-001 / X-001 severity | V3: P1 | Conceded to P2 by V3 (R2-A3 row 1); X-001 V3 at 92% on evidence, at P2. The card's P1 is INV-019, a different path |
| C-001 option (b) as the fix | V2 advocate: narrow plan:133 only | The P2 author reads only the spec, so the false FAIL would stay in the one sentence that matters (V3 advocate R2). Kept as the fallback if the owner declines |
| V1 parenthesis + V3 Edit 2 as written | Round 2 proposal | Superseded by part A, which reaches the same carve-outs by placing the existence check inside the required clause and also fixes INV-011 and INV-019 |
| C-002 / X-003 severity | V2: P1 | Conceded (R2-A2 row 1); a Constraints line cannot be breached by a diff (`qa.md:310,318,339`) |
| C-004 / R3-2 | V3: Task 7 bullet 3 fails because of the earlier package | Premise false; the index shows `...001016` staged (re-checked this step); withdrawn (R2-A3 row 4) |
| C-004 / R2-3, Tier 1 card R-2 | Allow new `.dev/reflect/` or `.dev/implement/` lines in Task 7 bullet 3 | Exposure small (collapsed `??` lines; executor ledger stays in the package, `implement.md:58`); widening breaks F-2's "reads exactly the quoted text" verifier (brief:55) |
| C-011 / R3-7 | V3: add "Depends on: Task 1" to Tasks 2, 3, 6 | Executor runs in source order (`sc-implement-protocol/SKILL.md:97`); withdrawn (R2-A3 row 7) |
| C-006 exit-code half | V1: append `echo exit=$?` to every log | `make` prints `Error N` on failure (R2-A1 row 9); only the format-check half is kept (M-09) |
| C-005 Task 5 half | V1: plan:111 has the same vacuity | Withdrawn: plan:111 uses the full path (R2-A1 row 6) |
| C-007 qualifier in the sentence | Add "with `--output`" to the live-check sentence | Conforming briefs pass `--output` (spec:142); note only (M-12) |
| C-008 twin edit | Edit `WORKER-CONTRACT.md:24` | Seventh file, outside plan:21; note only (M-13) |
| C-009 routing wording | Reword brief:230's tail | Brief-owned text under F-3's byte-for-byte rule; owner note (M-14) |
| INV-017, INV-020, INV-021 | Probe suggestions | See "Invariant probe disposition" |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|---|---|---|---|
| 1 | Low | C-001 evidence misattributed | Restore V1 A-2 evidence |
| 2 | Medium | A P1 that rests on an INFERRED path may be over-priced | Drop M-01 to P2; the wording fix still stands |
| 3 | Medium | New sentence carries an unforeseen false FAIL | Fall back to V1's parenthesis plus V3's Edits 2-3 (probe-checked, INV-012 ADDRESSED); INV-019 then stays open |
| 4 | Low | Risk list out of step with the sentence | Revert to brief:239-241 text |
| 5 | Low | Pin not unique | Choose another substring unique to part A |
| 6-13 | Low | Additive notes | Remove the note |
| 14 | Low | Base finding lost | Restore the V1 original from `variant-1-original.md` |

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved (`--interactive`)
- Approved by: auto
- Approval timestamp: 2026-11-06T04:12Z
