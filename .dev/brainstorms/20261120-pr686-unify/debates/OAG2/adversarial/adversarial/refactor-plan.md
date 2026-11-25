# Refactoring Plan: OAG2

## Overview

- Base variant: Variant 1 (OURS), `variant-1-original.md`
- Incorporated from Variant 2: 6 changes (1, 3 to 6 and 7 below; change 2 is an orchestrator correction found after Round 1)
- Rejected: 4 (see "Changes NOT Being Made")
- Overall risk: Low, with one Medium (change 3, the file pair)
- Output of the merge: a recommendation document (not a revised position paper) that answers OA-9, OA-17a and OA-17b separately, so the merge-executor works from the base's structure but rewrites each part as a decision plus the conditions the spec must state.

## Planned Changes

### Change 1: Reader selection rule, window shown on screen
- Source: Variant 2 fact 1 (C-003, 75%), Variant 2 advocate's "newest file may be the report's" point, Variant 1 hybrid (U-003).
- Target: base Mechanism and the "window problem" risk bullet; replaces "The spec must say who passes which `--window`".
- Approach: replace. Rule: the file already carries `observed_at`, `window` and `scope.root`. The observer reads the newest `*-sweep.json` whose `scope.root` equals its own root, and shows `window`, `observed_at` and the age. The work report does not read a file whose `window` is shorter than the time since its previous report; it runs `superclaude sweep run --window <that time>` itself, which also saves a file. The coordinator keeps WC-16's one sweep per 5 minutes.
- Rationale: C-003 and X-002; both advocates.
- Risk: Low to Medium (the observer may show a report-made file with a long window; the window shown on screen keeps this honest).

### Change 2: Correct the premise that the file must be taught to record its window and root
- Source: orchestrator check after Round 1 (`sweep/report.py:621-631`, `_window_text` at `report.py:95-101`); not in either paper.
- Target: base Mechanism.
- Approach: insert a sentence: JSON v1 already holds `observed_at`, `scope.root` and `window`; no new field is needed for this; the missing part is the selection rule of change 1. The new fields of D11 (`session_id`, `worktree_path`) are a separate item.
- Risk: Low.

### Change 3: Pair rule for the file and its Markdown
- Source: Variant 1 advocate's concession (`commands.py:182`, `MAX_SUFFIX = 99`).
- Target: base Mechanism ("a second file with the same stem").
- Approach: replace "the same stem" with "the same stem and the same suffix (`<UTC>-sweep.json` pairs with `<UTC>-sweep.md`, `<UTC>-sweep-2.json` with `<UTC>-sweep-2.md`)"; the `.md` link stays the commit point; the contract note decides what happens when the JSON cannot be written, and a test pins that a pair always shares its suffix.
- Risk: Medium (touches a tested publish path; a mismatch would give a reader the wrong pair).

### Change 4: Entry text allowlist, cap and fallback
- Source: Variant 2 facts 3, 5 (C-006, C-007, C-008), A-001.
- Target: base claim 2 and the entry-fields risk bullet.
- Approach: replace "shows entry text ... always through sanitize.py" with: the observer shows entry fields from a named allowlist; `recommend` and `suggested` are never shown; `how` is not shown until the owner has reviewed what it holds (UNVERIFIED); every shown field is `rich.Text` built from data; block fields have a length cap (the renderer clips lines by width, `render.py:158-160,325`, but its wrap helper never truncates, `render.py:85`). While the entry writer (`superclaude orchestrator report-entry`) is absent the observer shows titles and links only. The three states stay distinct. Tests: a fixture with `recommend` and `suggested` filled shows neither; a 5,000-character field shows at most the cap; bracket markup shows literally.
- Risk: Low.

### Change 5: Label and follow-up for the questions exception
- Source: Variant 2 facts 7 and 8 (C-009, C-010, C-011).
- Target: base claim 3 and the cost line "A one-line label".
- Approach: replace the label with: "questions read from Orca directly; a question already handled can appear as open" (`questions.py:9-12`). Replace "one data source" with the qualified sentence "one source for session facts (the sweep); the questions panel is the one exception". Add a tracked follow-up (the owner names the owner of it) for one shared question id that also ends the two question channels of D11; it is not a precondition of the observer release.
- Risk: Low.

### Change 6: Qualify the 90 s argument
- Source: A-003 (both advocates QUALIFY).
- Target: base fact 2.
- Approach: replace "cannot fit" with "is not guaranteed to fit": `Budget(total_s=90.0)` is a cap, not a measured time; the case for a shared file rests on cost (a second Orca-and-transcript collection per cycle) and on WC-16, not on the 90 s figure.
- Risk: Low.

### Change 7: Gate on the entry writer and record the open claim about Clay's views
- Source: A-001, S-002.
- Target: base Claim and a closing note.
- Approach: insert: OA-17a text on screen is conditional on the entry writer landing (A-001, techref lines 805, 820); state that Clay's own views on OA-9 and OA-17 are not on record (UNVERIFIED), so the alternative was argued from TOPICS.md and the merged work.
- Risk: Low.

## Changes NOT Being Made

| Diff point | Variant 2 approach | Why the base approach stands | Evidence |
|---|---|---|---|
| C-001 | No sweep file; each reader collects for itself | The observer would get no sweep classes at all; both advocates concede; the file is the only cheap route to "the same facts in the same way" | `probes.py:130` against `collector.py:28-29`; V2 advocate concession 1 |
| C-006 | Titles and links only, permanently | Loses the plain-English screen the person asked for on issue 409; an allowlist gives the safety at lower cost; kept only as a fallback while the writer is absent | V2 advocate concession 2; Variant 1 strength 6 |
| C-009 | End the questions exception now, design the shared block before the observer ships | A design that does not exist would sit on the observer's release path; both advocates agree the follow-up is right, the precondition is not | V2 advocate concession 3; `report.py:613-640` (no questions block) |
| C-005, X-001 | A second persisted artifact breaches the read-only contract and grows the disk footprint | The Will Not line governs the skill session, not the command's own report write; the Markdown report is already written the same way; a retention gap, if real, covers the folder, not the JSON (UNVERIFIED) | `SKILL.md:62`; V2 advocate concession 5 |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 1 | Low to Medium | The observer shows a classification built for another reader's window | The window is on screen; drop to "newest file the coordinator made" |
| 2 | Low | None; removes a false gap | Revert the sentence |
| 3 | Medium | A reader gets a mismatched pair | Revert to the stdout-only JSON of today |
| 4 | Low | A field reaches the screen that should not | The allowlist is a list; shorten it |
| 5 | Low | The label understates or overstates the limit | Reword the label |
| 6 | Low | None | Revert the sentence |
| 7 | Low | None | Revert the sentence |

## Review Status

Approval: auto-approved (unattended run, no `--interactive`). Timestamp: 2026-11-20.
