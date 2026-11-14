# Diff Analysis: owner-answer proposals for Q10 (may the sweep read Orca's pending questions)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C; Mode A copies)
- Total differences found: 14
- Categories: structural (1), content (5), contradictions (2), unique (3), shared assumptions (2 promoted, 1 stated)
- Prerequisites validated: output path is under `.dev/`, not a forbidden `.claude/` prefix; all three inputs exist.
- Orchestrator fact check (2026-11-14): `report.py:199` is the header line `"Messages coverage: partial"` (pinned by `tests/sweep/test_report.py:590`, shown in the design at `docs/designs/orchestrator-mode.md:610`); `report.py:534-535` is the bullet "Messages coverage is partial: pending questions cannot be read without consuming them". The sweep's allow-list (`probes.py:49-60`) has no `check` verb.

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Section set | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | May the sweep ever read questions? | Yes, after OB-03 and OB-04 pass and the build is pinned, through one owner-signed template | Never, as a standing rule | Not for now; reopenable by the owner | High |
| C-002 | When the two sweep sentences change | Now, in SW-07 | Once, after OB-03 gives a result | Now, in SW-07 | Medium |
| C-003 | Allow-list (NFR-014) change | An eleventh template later | None, ever | None now | High |
| C-004 | Division of labour between observer and sweep | Both may read questions | Observer only, permanently | Observer only, for now | Medium |
| C-005 | Dependence on the live tests (OB-03, OB-04) | The allow-list change depends on them | The wording fix depends on them | None | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact |
|---|---|---|---|---|---|
| X-001 | If consumption is disproven, should the sweep read questions? | Yes: the sweep runs in the coordinator's own session, the only terminal that can read its Run | No: "'Never' rules out the sweep reading questions even if consumption is disproven" (accepted as a cost) | Left open | High |
| X-002 | Is an interim "not established" sentence better than leaving the current text until the fact is known? | Interim sentence now | Keep the current text (which ADJ says overstates, X-016) until OB-03, then change once | Interim sentence now | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | A | The sweep runs inside the coordinator's own session, which holds the Run, so it is the one place a question read could work for the coordinator (gate test Q-1 failed: only the holder terminal can read) | Medium |
| U-002 | B | A permanent division of labour (sweep: workers and worktrees; observer: questions) and a single wording change | Medium |
| U-003 | C | Zero cost: matches the spec default and lets SW-07 proceed in W3 | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three treat "the sweep's two sentences" as one replaceable text | Both places can take the same three-sentence replacement; but line 199 is a short header value ("Messages coverage: partial") pinned by a test and shown in the design, while lines 534-535 are a bullet | UNSTATED | Yes |
| A-002 | All three leave questions with the observer (A adds the sweep later) | The observer's questions read will actually be switched on; if Q6 parks it, no program shows the coordinator its questions | UNSTATED | Yes |
| A-003 | All three | `check` is not in the sweep's allow-list today (`probes.py:49-60`) | STATED | No |

### Promoted shared assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Both report lines take the same replacement text | All three | If false, SW-07's acceptance text needs one wording for the header value and one for the bullet, and the design line 610 changes too | Open |
| A-002 | The observer will eventually read questions | All three | If false, "observer's alone" means "nobody", and the coordinator's only question view is Orca itself | Open (depends on Q6) |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 3
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, X-001
- Taxonomy tags: L3 (guard and state): C-001, C-003, X-001, A-001; L2 (structure and dependency): C-002, C-004, C-005, X-002, A-002; L1: S-001.
