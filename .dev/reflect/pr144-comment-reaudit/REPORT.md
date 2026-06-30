# /sc:reflect UC-2 — PR #144 comment re-audit + remediation (804eb4f4)

- **Mode:** post (UC-2) · **Tier:** 2 (deep; 2 heterogeneous adversarial reviewers: opus/skeptic + sonnet/qa)
- **Input:** PR #144 comment 4650256274 (clayphi) → resolved to diff `348e9400..804eb4f4`
- **Worktree:** `/config/workspace/IronClaude-pr144-reflect` (HEAD advanced to the remediation commit)
- **Calibrated confidence:** 0.93 · **Status:** success (validated + remediated; reviewers 0.94 / 0.91)

## What the comment asked
clayphi (convergence author) accepted all of FU-1/FU-2 and the restorations, and raised ONE new intentional decision: commit `804eb4f4` deliberately **removes TB-Add-2** (item-count bounds, caps tasks at 40 items/track + "promote to blocking" — incompatible with their 100-250+ item task files; the convergence task itself had 253 items), keeping **stable TB-Add IDs with a gap (1, 3-8)**. Asked to **supersede the TB-Add-2 guards** (same pattern as exec-context), not re-restore. Plus a consistency note: the A.10.5 INV-010 orphan lever was re-pointed `halt-A.10-before-A.10.5` → `retry-into-max-cycle-then-Open-Questions` (DET-015/DM-005).

## Validation verdict
- **clayphi's 804eb4f4 is internally consistent and intent-faithful** — TB-Add-2 stripped from rf-qa.md catalogue + SKILL.md A.10 prompt + validation checklist; list renumbered contiguously; LIVE_TB_ADD example → `[TB-Add-1, TB-Add-3, …]`.
- **A.10.5 anchor change VALIDATED (not invented):** `retry-into-max-cycle-then-Open-Questions` is the published DM-005 wire value at `SKILL.md:1632`, tied to the DET-015 no-halt decision at `SKILL.md:1648`. No extant `halt-A.10-before-A.10.5` lever remains. ✓
- **Stable-ID-with-gap design ACCEPTED (both reviewers):** the INV-010 runtime mechanism (`extract_catalogue` = dedupe + sort-by-N) is **contiguity-agnostic** (empirically proven on the gapped catalogue + a synthetic TB-Add-9). No consumer indexes TB-Add by ordinal position — all use the ID or `TB-Add-*` wildcard. Renumbering 3-8→2-7 would orphan **~169 cross-references** for zero runtime benefit → the gap is the correct, lower-risk choice.

## Blast radius beyond clayphi's named guards (the high-value finding)
clayphi named only the *PR06 TB-Add-2 assertions + checklist-count + INV-010 anchor*. The removal actually broke **13 guards** (5 merge + 8 audit) because several encode a **contiguity/density invariant** (the M1 "freeze TB-Add-1..8" constraint) clayphi's comment didn't mention, plus **clayphi's commit left two source-side inconsistencies**:

1. **rf-qa.md:302 `#### Checklist (28 items)` was stale** — the renumber left it at 28 but there are now **27** items (last item `27. TB-Add-8`). Source-side off-by-one in clayphi's own commit. **Fixed** (28→27) — completing the renumber.
2. The hidden-input guard's only `.dev/tasks/done/` mention (TB-Add-2's advisory line) is now **gone** → guard re-baselined `==1` → `==0` (a *stronger* no-hidden-input posture; both reviewers confirmed `==0 > <=1`).

## Remediation applied (15 test-side supersessions + 1 source completion; clayphi's behavioral change stands)
| File | Change |
|------|--------|
| `src/superclaude/agents/rf-qa.md` | checklist heading `28 items` → `27 items` (complete the renumber) |
| `tests/skills/test_task_builder_merge.py` | drop TB-Add-2 from 3 param/tuple lists; `test_tb_add_2_marked_advisory` → `test_tb_add_2_removed_deliberately` (absence guard); drop `check 13` from traceability; 2× count `28`→`27` |
| `tests/audit/test_dynamic_enumeration_inv_010.py` | `MIN_LIVE_K` 8→7; `is_dense`(contiguous) → `is_well_formed`(unique+sorted); fixture `synth_n = max+1` (was `k1+1`, collided with TB-Add-8); AC-4 allowlist `{1,2}`→`{1,3}` (×2) + docstrings |
| `tests/audit/test_sequencing_PR06_before_PR04.py` | `MIN_LIVE_K` 8→7; `is_dense` → `is_well_formed` (unique+sorted) |
| `tests/audit/test_hidden_input_guard.py` | `done_mention_is_advisory_only` (==1) → `has_no_done_mention` (==0); class docstring |

**No source-side bug masked** (both reviewers): the `synth_n=max+1` change is a fixture-correctness fix (the mechanism handles gaps); `is_dense`→`is_well_formed` preserves the real invariant (no dupes, sorted) and drops only the fake contiguity over-constraint.

## Verification
- `tests/skills/test_task_builder_merge.py`: **66 passed** (was 5 failed).
- `tests/audit/`: **1188 passed**, only the pre-existing filesystem `test_task_id_naming_pattern_preserved` fails (unrelated; known set).
- `make verify-sync` green · `ruff format --check` + `ruff check` clean.

## Deviation classification (of clayphi's 804eb4f4 vs. its stated intent)
- **Necessary (authorized supersession):** TB-Add-2 removal + renumber + A.10.5 anchor re-point — maintainer-authorized, coherent, validated. 0 regressions.
- **Drift (minor, in clayphi's commit):** stale `28 items` heading (incomplete renumber) — **remediated** here.

`regression_present: false` · `unauthorized_deviation_present: false` · `needs_human_decision: false`.
