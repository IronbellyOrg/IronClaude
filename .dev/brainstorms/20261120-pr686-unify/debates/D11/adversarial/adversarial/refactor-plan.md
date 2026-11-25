# Refactoring Plan: merge OURS and the debate outcome into the CLAY base (D11)

## Overview
- Base variant: Variant 2 (CLAY, `variant-2-original.md`), score 0.8667 against 0.7723.
- Incorporated: Variant 1 (OURS, `variant-1-original.md`) strengths, the Round 2 per-point outcomes (`debate-transcript.md`), and the invariant probe (`invariant-probe.md`).
- Planned changes: 10; rejected alternatives: 6.
- Overall risk: Medium (the base's claim and mechanism are rewritten; the facts and the cost list are kept).
- Output file: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/adversarial/merged-d11-observability-recommendation.md`.
- Every fact in the merged file must carry its source (file:line, PR or issue number). Do not invent a fact. Anything marked UNVERIFIED in the inputs stays UNVERIFIED.

## Planned Changes

### Change 1: Replace the claim paragraph (replace; Medium)
- Source: OURS "The claim" plus debate outcome X-001, C-002, C-003 (HYBRID, CLAY on C-003).
- Target: base section "The claim".
- Text to write: the sweep JSON (schema v1) is the one source of session facts; the observer is the one screen; the work report is the one plain-English report and the work-item layer (GitHub, ClickUp, per-issue text), and it meets Clay's issue 409 asks today. Adopt the report's features as listed in Change 9. Do not hold the working report behind unwritten design.
- Rationale: C-003 (CLAY 80%), X-001 (HYBRID 73%), C-002 (HYBRID 75%).

### Change 2: Replace "The mechanism" with a three-layer data flow (restructure; Medium)
- Source: OURS "The mechanism" (layers) and CLAY mechanism items 1 to 3 (entry files, join, table); X-001, X-002.
- Target: base "The mechanism".
- Text: Layer 1 facts (sweep JSON); Layer 2 work items (report skill: entry files, join, sort, compare, `check.py` gate); Layer 3 screen (observer reads sweep JSON for sessions and entry files for work items); notice step (nine rows, cap). Direction: session facts flow sweep to report; work items flow report to observer.
- Rationale: X-001 HYBRID.

### Change 3: Add a section "Testable rules for the spec" (insert; Medium)
Rules, each testable, with the finding that forces it:
1. The sweep JSON v1 row gains `session_id` (and `worktree_path`) as additive fields, allowed to be empty; a reviewed edit to the golden test (NFR-009, `docs/designs/orchestrator-mode.md:605`). `row_id` is not a contract (INV-003; `classify.py:903,933`).
2. One session shown as two rows (an Orca row and a transcript row) is merged by `session_id` where both have one (INV-003).
3. The sweep JSON is saved as a file next to the Markdown report, or the spec says each consumer runs its own sweep; WC-16 bounds sweeps to one per 5 minutes, the observer polls every 15 s (INV-006).
4. The report passes `--window` equal to the time since the previous report (24 h on the first run); "idle" in the sweep window never means "no progress since the previous report" (INV-007).
5. HIGH, INV-001: the report reads transcripts for the session ids in the sweep rows PLUS every not-done session of the previous report even when its terminal or worktree is gone; a session is closed only by a source-confirmed reason, as today (`sessions.py:378-400`).
6. HIGH, INV-002: before the report's own terminal-to-session map (`orca terminal list` plus the Orca hook file) is removed, one live side-by-side run compares the sessions both maps find; the old map stays until the sweep's `orca-tabs` map finds every session the old one finds (UNVERIFIED which covers more). A fixture test alone does not satisfy this.
7. "Orca unavailable" or "sweep failed" is written as `read: false` in the report's session step; the previous reads are skipped, never read as "sessions ended" (INV-004; `sessions.py:282-306,77-96`).
8. The report skips the coordinator's own workspace session; the counts of the two tools are compared only after that skip; totals from the sweep are lower bounds (INV-010).
9. The observer's coordinator-questions panel is a second Orca reader (`adapter.py:32`). The spec states it as an accepted exception, or the sweep gains a questions block; the owner decides (INV-005).
10. One question gets one id across the observer (Run, message id), the sweep (`row_id`) and the report (issue URL), or the three are shown as separate lists; no duplicate "Needs you" and question row (INV-009).
11. Entry files store only `session_id`; the class is read from the sweep at display time (INV-008).
12. Observer shows text from entry files only after `observe/sanitize.py`; empty `orchestrated/` and zero sweep rows each show an explicit "none", separate from "could not read"; a list cut at the 100-row page or show cap says "lower bound" (INV-012).

### Change 4: Read-only and "recommend nothing" rules (insert; Low)
- Source: OURS C-004 (OURS 83%).
- Text: the sweep (`sc-sweep-protocol/SKILL.md:61`) and the observer (navigation only, issue 409 item 2) carry no Options, no Recommendation and no write. Options, Recommendation, the typed answer, the ClickUp DM and the commit of the report's own state folder belong to the report or the orchestrator session only. Whether the observer may show an entry's text word for word, labelled as from the report: owner decision (UNVERIFIED).

### Change 5: Person-specific values and naming (modify; Low)
- Source: OURS C-005, C-010 (73% each); CLAY concessions.
- Text: `person`, time zone, ClickUp user and token and the DM channel move to per-user config; the shipped `config.json` names no person. The skill's text follows the owner's naming (coordinator, not orchestrator) and layout (`.dev/coordinators/`); D08 settles the final name. The report still needs `$AWR_ROOT` or `orchestrator_repo` (`common.py:35-50`), so it is not zero-setup (A-004).

### Change 6: Nine-row table (modify; Low)
- Source: C-006 HYBRID 75%; A-002.
- Text: adopted with "the person" instead of Clay; it lives in the notice step only; the sweep and the observer never pick a row, they may show the row number an entry already records; the planned test "exactly nine rows" is kept (`docs/designs/orchestrator.md:1116`). Rows 1 to 7 are never low-stakes.

### Change 7: Cap of 5 notices a day (modify; Low)
- Source: C-007 HYBRID leaning OURS 63%; INV-011.
- Text: adopted as a PROPOSED default of 5 per repo per 24 hours, notices only, entries never dropped. It is not "settled": ruling 39 is Clay's, AD-B4 calls it "not ruled on; open" (`orchestrator.md:1177`), the parser returns 0 (no cap) for an absent key (`pr-a issue_watch/repos.py:262-269`), and `escalate` and `asks.json` do not exist. No generator writes a value until the owner records a ruling.

### Change 8: Living report and status words (modify; Medium)
- Source: C-009 HYBRID 72%; C-008 OURS 78%; INV-008.
- Text: adopt entry files with a per-user, configurable state path and `refresh` with no model call; the six work-item words (working, progressed, waiting on you, stuck, stalled, done) stay for work items only; any session state on the screen is the sweep's class word for word.

### Change 9: Add the adoption table for Clay's features (insert; Low)
Rows: living report (adopt with change), nine rows (adopt with change), cap of 5 (adopt as a proposal, not settled), silent-loss check (adopt as is, in the report layer so the sweep stays stateless), plain-English item template (adopt with change: generic wording), `check.py` gate (adopt as is).

### Change 10: Keep and extend costs and risks; add open decisions for the owner (modify; Low)
- Keep the base's cost and risk lists; add: the JSON field and golden-test edit; the two-map coverage check; the observer questions exception; the cap ruling. Add a section "Open decisions for the owner" (one question each): cap value and who rules; observer showing entry text; observer questions panel as exception or a sweep questions block; where the sweep JSON file lives.

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected | Debate evidence |
|------------|-------------------|--------------|-----------------|
| X-001 (reverse) | CLAY: the report is a node the sweep and observer "feed or read" for session facts | Reverses the stability order: a one-person, model-using, writing skill would sit under zero-token read-only tools | OURS 75% in Round 1; CLAY advocate conceded (X-001 HYBRID 75%) |
| C-001 | CLAY: keep the report's own session finder and status logic | Two status vocabularies for one session; model-decided status is weaker than written proof rules | CLAY advocate: `sessions.py:5-6`; split decided at C-001 HYBRID |
| C-004 | CLAY: Options and Recommendation visible on all surfaces | Sweep "Will Not: recommend anything" | CLAY conceded 85% |
| C-007 | CLAY: cap of 5 as "settled" | Ruling is Clay's; AD-B4 open; nothing enforces it | both advocates 60-65% |
| OURS C-009 silence | OURS: say nothing on the living report | CLAY shows a clear separable benefit (no-model refresh, no double reporting) | OURS conceded |
| X-002 (OURS) | OURS: write the contract note and test first, report waits | Holds a working tool for an unwritten note | OURS conceded "do not freeze" |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1, 2 | Medium | Rewrites base claim and mechanism | Restore from `variant-2-original.md` |
| 3 | Medium | Adds many requirements; a wrong one misleads the spec | Each rule cites one finding; drop a rule without touching others |
| 4 to 7, 9, 10 | Low | Additive or wording | Delete the inserted block |
| 8 | Medium | Changes what the screen shows for a session | Restore the base sentence |

## Review Status
- Approval: auto-approved (non-interactive). Timestamp: 2026-11-20.
