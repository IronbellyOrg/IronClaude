# Refactoring Plan: Q9 merged answer

## Overview
- Base variant: variant-1-original.md (proposal A)
- Incorporated variants: proposal B (one change), proposal C (one change); one caveat from the shared-assumption responses
- Planned changes: 3
- Overall risk: Low
- Merged output path: ../merged-answer.md (in the Q09 folder)

## Planned Changes

### Change 1: an ordered Phase 2 fallback with the embedded form before any sidecar
- Source: proposal B (append the JSON object to the dated report), corrected by B's own advocate.
- Target: base "What happens next", third and fourth bullets.
- Approach: modify. When triggered, try in order: (1) caller capture of stdout; (2) embed the JSON object inside the one dated report, placed before the `Report complete` footer (a pinned test, `tests/sweep/test_cli_contract.py:1476`, requires the report to end with it), with a fence that cannot be closed by backticks in worker-written text (the existing `sanitize`, `report.py:569-599`, does not touch backticks) and a test that the embedded and stdout copies match apart from `report_path`; (3) only then a separate file, which relaxes NFR-001 and changes its design line, two tests and the contract-note registry in one PR.
- Rationale: C-002 (B, 60%), C-004 (B, 85%), X-002 (B, 90%); all three advocates' verdicts.
- Risk: Low.

### Change 2: record now that the JSON has no stored form
- Source: proposal C, "What happens next" third bullet.
- Target: base "What happens next" (new first bullet).
- Approach: insert. The contract note (XC-05) states: "sweep report JSON v1 is a stdout-only reply; it has no stored form until a named reader triggers SW-11."
- Rationale: C's advocate verdict; removes ambiguity without closing the door.
- Risk: Low.

### Change 3: durability and host caveats
- Source: diff-analysis A-001 and A-002 and all three responses (B REJECTed A-001).
- Target: base "What it costs or risks" (new bullet) and "What stays unresolved".
- Approach: insert. Reports live in the gitignored `.dev/sweeps/` folder and are deleted by hand (`.gitignore:256`; design `docs/designs/orchestrator-mode.md:35`), so "read the Markdown report" is a best-effort look-back, not a durable record, and an embedded copy is only as durable as its report. The trigger asks the first reader which host it runs on: a reader on another host (for example a Coder#477 status record) needs a transport none of these options provides.
- Rationale: A-001 (A, 65%), A-002 (A, 80%).
- Risk: Low.

## Base weaknesses addressed
| Issue | Better variant | Fix |
|---|---|---|
| The stored fallback jumped straight to relaxing NFR-001 | B | Change 1 |
| Nothing written now says the JSON is not stored | C | Change 2 |
| Report durability and remote readers unaddressed | shared-assumption responses | Change 3 |

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, X-001 | B: embed now | No named reader (merged-requirements.md:221); unanimous for A |
| C-001, C-003, C-005 | C: never, close SW-11 | Contradicts ADJ A-001 (78 percent) and the conditional V2-04 link (:401); C's own advocate voted A |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | Planning order only; no code now | Edit text |
| 2 | Low | One sentence in a planned note | Remove |
| 3 | Low | Caveats | Remove |

## Review Status
Auto-approved, 2026-11-14 (non-interactive).
