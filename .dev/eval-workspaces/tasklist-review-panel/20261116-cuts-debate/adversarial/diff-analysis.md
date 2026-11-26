# Diff analysis: proposed cuts C1 to C9, variant 1 (Sonnet, analyzer) against variant 2 (Haiku, architect)

Context for a reader with no history: see `../source-proposed-cuts.md`. This is Step 1 of `/sc:adversarial` at depth quick, Mode B with two generated variants (two, not three, because the owner's two-session limit leaves one slot while the Recipe Ledger session runs its hold-out). Written by the orchestrating session, not by an advocate.

## Metadata
- Variants compared: 2
- Differences: structural 1, content 6, contradictions 2, unique contributions 6, shared assumptions 3
- Taxonomy levels: L1 surface 0, L2 structural 6, L3 state mechanics 3 (running experiment, freeze hashes, anchors)

## Structural differences
| # | Area | V1 | V2 | Severity |
|---|---|---|---|---|
| S-001 | Format | Verdicts plus ranked list, evidence-heavy | Verdicts plus ranked list, policy-heavy | Low |

## Content differences (verdict per cut; agreement in bold)
| # | Cut | V1 | V2 | Severity |
|---|---|---|---|---|
| C-001 | C1 open-list trim | **CUT NOW** in place, keep names and numbering | **CUT NOW** status-only, keep anchors | Low (agree; V2 adds: keep RL's freeze and maintainer-test questions) |
| C-002 | C2 hook design replace | CUT NOW: document swap with a SUPERSEDED header | CUT LATER: the smallest version drops owner-required behaviours | **High** |
| C-003 | C3 build model-report | CUT LATER (Opus judging would be flagged; needs allow-by-role) | CUT LATER (new work, no authorisation, estimate unproven) | Low (agree) |
| C-004 | C4 RL machinery | CUT LATER, four unreferenced fragments after hold-out | KEEP: never-used argument expired; D1-D7 registered | Medium |
| C-005 | C5 re-ask and spikes | **KEEP** | **KEEP** | Low (agree) |
| C-006 | C6 archive stopped folders | CUT LATER (collab half when hold-out idle) | CUT LATER after reference migration | Medium |
| C-007 | C7 foreign scripts | **KEEP** | **KEEP** | Low (agree) |
| C-008 | C8 allowances | **KEEP** | **KEEP** | Low (agree) |
| C-009 | C9 unbuilt plan package | CUT LATER: stage it, never delete; archive on owner's word | CUT NOW, label only (superseded notice, original intact) | Medium |

## Contradictions
| # | Point | V1 | V2 | Impact |
|---|---|---|---|---|
| X-001 | What the smallest hook version must cover | Pure document swap is safe because `model-report` does not exist | The 2026-11-16 answers require warnings for unknown, out-of-list, wrong-stage and served-versus-requested cases, plus explicit-user and approved-job exceptions, default fallback and installed-file protection; the audit's version only flags restricted Opus ids | High |
| X-002 | Whether the audit's code-cut claims are right | Not right: analyze.py is 1,587 lines and holds the D1 to D7 gates; non-test RL code is about 7,200 lines | Not right: registered addendum names D1 to D7 | Medium (the two variants agree the audit overstated C4) |

## Unique contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | RL freeze already exists (tag `rl-freeze-1553f5dd29b1`, 32 files hashed); `rl/reask.py` and `rl/spike.py` are in it; removing them breaks `freeze.sh --check` | High |
| U-002 | V1 | `freeze.sh` hashes `rl/*.py` but not `scaffold/`, so the format allowances are outside the freeze | High |
| U-003 | V1 | Four RL files appear unreferenced by the run path: `analysis/ran_check.py`, `bin/ran-audit.py`, `analysis/g0.py`, `bin/open-manual-checks.sh` | Medium |
| U-004 | V1 | The hook scan would flag the intended Opus blind judge unless it can allow by role | Medium |
| U-005 | V2 | Master lists are cited by frozen RL files and by `PROCESS.md`; keep anchors and RL's own open questions | Medium |
| U-006 | V2 | C9: label-only cancellation, original plan intact, only with owner authorisation | Low |

## Shared assumptions (unstated preconditions of the agreement points)
| A | Agreement point | Assumption | Class | Promoted |
|---|---|---|---|---|
| A-001 | C1 cut now | Editing the two master lists does not change any file hashed in `RL/config/freeze.json` | UNSTATED | Yes (L3) |
| A-002 | C5, C7, C8 keep | The running hold-out reads nothing outside the RL folder and the shared slot lock | UNSTATED | Yes (L3) |
| A-003 | All "reversible" claims | A `git mv` archive is cheap while another session is committing in the same worktree | UNSTATED | Yes (L2) |

## Summary
Highest-severity: C-002 (C2), X-001. The two variants agree on C1 (cut now), C5, C7, C8 (keep), C3 (not now). They differ on C2 (now or later), C4 and C6 (later or keep), C9 (label now or stage later).
