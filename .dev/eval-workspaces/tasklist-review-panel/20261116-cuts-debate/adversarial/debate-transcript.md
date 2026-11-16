# Debate transcript summary (depth quick: Round 1 only)

Full advocate statements: `debate/round1-advocate-1.md` (Sonnet, variant 1), `debate/round1-advocate-2.md` (Haiku alias, variant 2). Variants: `variant-1-sonnet-analyzer.md`, `variant-2-haiku-architect.md`. Rounds completed: 1. Round 2 skipped (depth quick). Round 2.5 invariant probe skipped (depth quick); the advocates raised two invariants themselves.

## Scoring matrix (per diff point)

| Diff point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 C1 trim | Both (cut now, labels, keep anchors) | 90% | Lists cited by frozen RL files; neither hashed in freeze.json (both advocates read it) |
| C-002 C2 hook | Variant 2 (header plus coverage proposal, no replacement) | 85% | Advocate 1 conceded the smaller version drops owner-required behaviours; both agree on the header |
| C-003 C3 build | Both (not now) | 85% | No `model-report` exists; owner decisions authorise no build; judge allow-by-role unsolved |
| C-004 C4 RL code | Variant 2 for now; variant 1 for fragments later | 90% | analyze.py is 1,587 lines with gates D1 to D7 registered; hold-out running |
| C-005 C5 | Both (keep) | 95% | Frozen files; launcher calls re-ask |
| C-006 C6 archive | Both (later) | 85% | `git mv` of 1,620 files lands in the shared index; copy-shared.sh and reading lists cite the folders |
| C-007 C7 | Both (keep) | 90% | Tracked and cited; keep-intermediates rule |
| C-008 C8 | Both (keep) | 95% | Registered; strict reading fails 47 of 81 |
| C-009 C9 | Variant 2 (retain, label only on the owner's word) | 75% | Untracked, unexecuted; never move to done/ |
| A-001 | ACCEPT (both) | 90% | freeze.json hashes 32 files; none are the master lists |
| A-002 | QUALIFY or REJECT (both: not folder-local) | 85% | Author launchers read other folders; later runs run from the RL folder |
| A-003 | REJECT (both) | 80% | Shared index; advocate 1 saw 12 staged files, advocate 2 saw an empty index; the staged state is volatile, which supports the rejection |

## Convergence assessment
- Points resolved: 12 of 12 (direction). Alignment 100% after concessions. Threshold 0.80 (quick default). Status: CONVERGED, with the caveat in `final-cuts.md`.
- Taxonomy: L2 structural (cuts) and L3 state mechanics (freeze hashes, shared index, running experiment) both covered. L1 surface: none.
- Unresolved points: none on direction. Open: the volatile staged-file claim (A-003 evidence conflict), recorded not resolved.
