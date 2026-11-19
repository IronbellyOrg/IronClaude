# Refactor Plan (Step 4)

## Overview

- Base: Variant 1 (variant-1-original.md, reviewer 1, analyzer). Combined score 0.961 against 0.822 for Variant 2 (see base-selection.md). Tiebreaker not applied.
- Incorporated variant: Variant 2 (variant-2-original.md, reviewer 2, qa).
- Planned changes: 10 (8 take content from a variant or from the debate; 2 take content from the invariant probe).
- Output: one merged reflection-review card with sections header, Findings, Coverage verdict, Risks, Recommendation, Open items.
- Overall risk: Low. The merged card keeps the shared verdict of both variants (accept the plan; nothing blocks). Every change adds, relabels or tightens text; none reverses a verdict.
- Invariant probe findings are not credited to either variant. They enter only through changes 9 and 10 and are labelled "from the invariant probe".

## Planned Changes

### Change 1: Findings F1 and F2 move from "minor" to "note"
- Source: Variant 1, Findings bullets 1 and 2; debate X-001 (won by Variant 2, 72%) and V1 advocate concession in round1-advocate-1.md ("F1 is weak", "F2 needs no action").
- Target in base: Findings, first two bullets.
- Approach: replace the severity label. Keep the text. State that both are wording points that cannot cause a wrong edit, because each number comes with a symbol name and plan:36 sets a measurable requirement.
- Rationale: both advocates agreed at the end of the debate that these are not decision-relevant. Confidence 0.80.
- Risk: Low.

### Change 2: The `IndexError` weakness becomes the lead Finding, labelled minor
- Source: Variant 1, F5 extension and "Risks" bullet 2; debate C-001 (Variant 1, 80%), X-002 (Variant 1, 85%); round2-advocate-1.md new evidence 2 and 3; round2-advocate-2.md new evidence.
- Target in base: Findings, F5 bullet; move it first and split it out of F5.
- Approach: restructure. Merge in these settled facts: plan:36 itself prescribes `message.split("NOT updated")[1]`; t2-checks.log:8-10 shows the `IndexError`; the older test uses the same pattern at test_how_we_work_install.py:113, so a consistent fix covers both lines; the weakness is readability only, because the supplied negative control still fails.
- Rationale: the one finding both advocates accepted as real and in scope. Confidence 0.85.
- Risk: Low.

### Change 3: Coverage verdict gains Variant 2's requirement-to-check mapping and log citations
- Source: Variant 2, Coverage verdict (all five bullets); debate C-004 (Variant 2, 82%), unique contribution U-005.
- Target in base: Coverage verdict; keep Variant 1's five bullets and append, per requirement, the acceptance check and the log range (`t2-checks.log:1-16`: nine passing file-level tests, lint clean, the cache-disabled failure, 352 passed with one skip; `source.md:1`; plan:24-30 and 32-40).
- Approach: append.
- Rationale: Variant 1 said "I could not run tests, so I have not confirmed that they pass" and never cited the log. Variant 2's log citations close that gap. Confidence 0.82.
- Risk: Low.

### Change 4: Add a provenance sentence for the supplied evidence
- Source: Variant 2 closing note and Coverage verdict; debate A-001 (QUALIFY, V2 discloses better, 78%).
- Target in base: Coverage verdict, last line.
- Approach: insert. Say: the test, lint and negative-control results are supplied evidence, corroborated by the logs agreeing with each other (351 then 352 passed is one new test) and with the code (the predicted `IndexError`), and not independently repeated by any reviewer.
- Rationale: neither reviewer ran anything; the base had only a partial disclosure. Confidence 0.78.
- Risk: Low.

### Change 5: Risks section adds Variant 2's existing-test safeguards as counter-evidence
- Source: Variant 2, Risks (three cases); debate C-002 (Variant 1 won, 75%, with the note that Variant 2's checks stay as counter-evidence), unique contribution U-004.
- Target in base: Risks, after the missed-risk items.
- Approach: append, as "checked and fine": unreadable or missing files (`install_keep.py:18-26`, `test_install_keep.py:38-45`); missing destination and forced install use the copy branch (`install_core.py:68-79`, tests at `test_how_we_work_install.py:28-34,79-99`); false-positive stale report (`test_how_we_work_install.py:102-115`).
- Rationale: stops the card from overstating risk. Confidence 0.75.
- Risk: Low.

### Change 6: The orca_worktree.py item is downgraded to an optional investigation lead
- Source: Variant 1 note (uncleared `filecmp.cmp` at `orca_worktree.py:480, 500, 1682`); debate C-003 (Variant 1, 65%), X-002; round2-advocate-1.md new evidence 1; round2-advocate-2.md ("remains an investigation lead").
- Target in base: Findings last bullet and the Recommendation's second sentence.
- Approach: replace. Keep the [INFERRED] tag. Add the verified context: line 500 follows `shutil.copyfile` at line 499, which writes a new modification time, so no stale hit is expected there; no path found that gives a wrong answer; a caller that runs `copy_issue_dir` and `stale_prompt` twice in one process was not checked. Drop "open a backlog issue" as a recommended action.
- Rationale: both advocates conceded it is a lead, not a defect. Confidence 0.80.
- Risk: Low.

### Change 7: Qualify the non-empty `PRINCIPLES.md` assumption
- Source: Variant 1 F2 text ("That works because PRINCIPLES.md is not empty"); debate A-003 (QUALIFY, credit to Variant 1, 91%).
- Target in base: Findings, F2 bullet.
- Approach: append one sentence. The byte change `shipped[0] ^ 1` (test:128) is valid while `PRINCIPLES.md` is shipped and non-empty (its line 1 is `# Software Engineering Principles`); no test guards that, and an empty file would raise `IndexError` before the installer is exercised.
- Rationale: both advocates ended on QUALIFY. Confidence 0.88.
- Risk: Low.

### Change 8: Recommendation is restated as one concrete action
- Source: Variant 1 Recommendation; debate C-003 and round2-advocate-1.md new evidence 3.
- Target in base: Recommendation.
- Approach: replace. Keep "accept the plan and implementation"; the one action is: in `tests/cli/test_how_we_work_install.py`, add `assert "NOT updated" in message, message` before line 134 and before line 113, then verify with `uv run pytest tests/cli/test_how_we_work_install.py -q`. State it is optional and non-blocking.
- Rationale: both advocates accepted the assert as valid and cheap; the second site comes from the V1 advocate's own round-2 point. Confidence 0.70 on the two-site version (the line-113 test already passes its own seeded case, so adding the assert there is a consistency choice).
- Risk: Low.

### Change 9: Carry the four settled MEDIUM invariant findings
- Source: invariant-probe.md INV-001, INV-002, INV-003, INV-008 (all UNADDRESSED, MEDIUM). Not in either variant.
- Target in base: a labelled block inside Findings, "Carried over from the invariant probe (not from either reviewer)".
- Approach: insert, one entry each, with the evidence and the cited lines:
  - INV-001: `filecmp.cmp` empties its whole cache once it holds more than 100 entries (the parent re-checked this against CPython source). The second call compares 8 files that sort before `PRINCIPLES.md` (`install_core.py:15-29, :59`). In a long test process with a full cache the purge could hide the old bug. The supplied failing run executed only this test (`t2-checks.log:7`, `-k same_size`).
  - INV-002: `test_how_we_work_install.py:125` ignores the first call's result; nothing checks that `PRINCIPLES.md` was skipped as identical, and lines 128-129 do not check that size and mtime still match `before` after the rewrite.
  - INV-003: no shipped CLI path compares the same pair twice in one process (`main.py:178` calls `install_core_files` once; `update` passes `force=True` at `main.py:365`, which copies without comparing, `install_core.py:71-77`). The bug is reachable only in-process. This changes priority, not correctness.
  - INV-008: `install_keep.py:3-7` says `install --force` and `update` back up a differing file first; `install_core.py:71-77` copies with `shutil.copy2` and no backup, and `update` always forces, so a user-edited `~/.claude/RULES.md` is overwritten with no copy (the parent re-checked this; `install_agents.py:56` and `install_templates.py:76` also copy without backup). Outside this plan's scope.
- Rationale: the gate did not block (0 HIGH UNADDRESSED), but the probe judged that both advocates shared the diff analysis's frame and missed these. Confidence 0.85 that they are real; the severity and the scope call stay with the probe.
- Risk: Medium-low. The only risk is readers taking these as findings by the reviewers, so each entry carries the label.

### Change 10: Add the two LOW unaddressed probe items and the INV-010 caveat to Open items
- Source: invariant-probe.md INV-006 (comments say "(size, mtime)" but the real key is path 1, path 2, type, size, mtime; `install_keep.py:20`, `test:119`), INV-012 (zero skipped files and exactly one stale file: no defect found), INV-010 caveat (the failing control run at `t2-checks.log:7` is a bare `pytest`, possibly another environment; the throwaway plugin was not saved; the one skipped test is unidentified).
- Target in base: new Open items list.
- Approach: append.
- Rationale: they are in the probe file and affect whether the evidence can be repeated. Confidence 0.70.
- Risk: Low.

## Changes NOT Being Made

| Rejected alternative | Why |
|---|---|
| Use Variant 2's Findings section ("None. No blocking, minor, or wording findings were established.") | Wrong as written: its own advocate conceded in round 2 that "no findings" is too absolute; the `IndexError` weakness is in the log it cites (debate C-001, S-001). |
| Use Variant 2's Risks section ("None found within the requested scope") | Wrong for the demonstrated readability risk (X-002, Variant 1 85%). Its three checks are kept as counter-evidence (change 5) but not as proof of "no risk". |
| Keep Variant 1's recommendation to open a backlog issue for `orca_worktree.py` | Both advocates conceded it is an investigation lead; no path was found that gives a wrong answer (change 6). |
| Keep F1 and F2 at "minor" | Settled as not decision-relevant (change 1). They stay, labelled "note". |
| Drop F3 and F4 | Both advocates confirmed them; they are cheap and correct. Kept unchanged as notes. |
| Credit either variant for INV-001, INV-002, INV-003, INV-008 | They are outside both texts (judge brief). They appear only as carried-over findings. |
| Re-open any debate point | All 9 points reached agreement; the C-003 reversal looked like mild deference (fault-finder), so it is recorded as the weakest preference, not re-argued. |
| Add new findings not present in the debate files | Out of the judge's scope. |

## Risk Summary

| Risk | Level | Mitigation |
|---|---|---|
| Carried-over probe findings read as reviewer findings | Medium-low | Each entry is labelled "from the invariant probe"; the merged card says neither variant raised them |
| The two-site assert recommendation (line 113 and line 134) widens a follow-up the first run did not propose | Low | Marked optional and non-blocking; the one-site version is named as the minimum |
| The `IndexError` finding promoted to lead may look like a bigger problem than it is | Low | The card says the negative control still fails and the bug is still detected; the issue is readability |
| Line numbers cited in the card go stale after later edits | Low | Each citation is paired with a symbol or quoted text; the card is a point-in-time review |
| Evidence is supplied, not reproduced | Low | Change 4 states it plainly; the Open items list names the unsaved plugin and the bare `pytest` run |

Overall: Low.

## Merged card outline (target of Changes 1 to 10)

Header: persona/model fields for both source reviewers; "merged from 2 reviewer cards by adversarial Mode A, base Variant 1"; converged 9 of 9 after round 2; probe gate not blocked.

Findings (severity-labelled):
1. minor: the new test fails with `IndexError` on `message.split("NOT updated")[1]` instead of a readable assertion (change 2).
2. note: F1 bare line numbers (change 1).
3. note: F2 unspecified byte change, plus the non-empty `PRINCIPLES.md` qualifier (changes 1 and 7).
4. note: F3 import order block (unchanged from the base).
5. note: F4 `same_content` clears the process-wide cache on every call; speed only (unchanged).
6. note: F5 negative control by disabling `filecmp.clear_cache` is a correct way to restore the old behaviour; one-off, not kept as a test (unchanged).
7. note: unreadable-file behaviour is unchanged by the switch; the only change is the cache clear (unchanged).
8. note, advisory, outside the spec: uncleared `filecmp.cmp` in `orca_worktree.py`; optional lead only (change 6).

Debate-settled positions to state in the card: S-001, C-001, C-002, C-003 to Variant 1; C-004 and X-001 to Variant 2; X-002 to Variant 1 (readability weakness only); A-001 and A-003 QUALIFY.

Carried over from the invariant probe (labelled): INV-001, INV-002, INV-003, INV-008, each MEDIUM with the evidence in change 9.

Coverage verdict: yes for all five requirements, with the mapping and log lines (changes 3 and 4).

Risks: the readability weakness; the three checked and fine cases (change 5); the probe items by reference; the sibling-file lead.

Recommendation: change 8.

Open items: whether to add the assert at one site or two; whether INV-001 warrants running the new test in a full suite with the fix reverted; whether INV-008 (no backup in `install_core`) should be filed as a separate issue; whether the orca lead is worth a look; INV-006 comment wording, INV-012 no defect, and the INV-010 caveats (change 10).

## Review Status

Auto-approved. Reason: no HIGH UNADDRESSED invariant findings, convergence 100% against the 80% threshold, and every planned change cites a debate or probe source. No change reverses a verdict.
