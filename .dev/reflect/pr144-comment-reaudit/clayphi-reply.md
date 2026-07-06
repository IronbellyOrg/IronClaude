### Re: TB-Add-2 supersession + conflict resolution — done

Validated `804eb4f4` via `/sc:reflect --mode post --depth deep` (2 heterogeneous adversarial reviewers) and applied the supersession you asked for. Branch is now **MERGEABLE**. Two commits:

**`7c86cbd5` — TB-Add-2 guard supersession (15 test edits + 1 source completion).** Your stable-ID-with-gap design (`TB-Add 1, 3-8`) is the right call and is confirmed sound: the INV-010 runtime mechanism (`extract_catalogue` = dedupe + sort-by-N) is **contiguity-agnostic** — empirically verified it auto-richens correctly on the gapped catalogue. Renumbering 3-8→2-7 to "close" the gap would have orphaned **~169 cross-references** for zero runtime benefit, so I kept the IDs stable as you intended. Your A.10.5 anchor change (`retry-into-max-cycle-then-Open-Questions`) checks out against the real DM-005/DET-015 contract (`SKILL.md:1632,1648`) — not invented.

Two things the removal touched that went **beyond the guards you named**, both handled:

1. **Blast radius was wider than the PR06 + checklist-count guards.** The removal also tripped the *density/contiguity* invariant in `test_dynamic_enumeration_inv_010.py` and `test_sequencing_PR06_before_PR04.py` (the M1 "freeze TB-Add-1..8" constraint): `MIN_LIVE_K 8→7`, and `is_dense` (asserted `[1..K]` contiguous) → `is_well_formed` (unique + sorted — the *real* invariant the mechanism enforces). Also fixed a fixture bug the gap exposed: `synth_n = k1+1` collided with the live `TB-Add-8` (count 7 ≠ max-ID 8) → now `max(N)+1`. And the AC-4 symbolic allowlist `{1,2}→{1,3}` to match your updated `LIVE_TB_ADD` example.

2. **One stale source-side count in `804eb4f4`:** `rf-qa.md:302` still read `#### Checklist (28 items)` after the renumber — it's now **27** items (last is `27. TB-Add-8`). Fixed the heading + the two count assertions, completing the renumber.

Bonus: removing TB-Add-2 deleted the *only* `.dev/tasks/done/` mention in `SKILL.md`, so I tightened the hidden-input guard from `== 1` (advisory exception) to `== 0` — a strictly stronger no-hidden-input posture.

**`2c20b970` — merged `master` to clear the PR conflict.** Sole conflict was `SKILL.md` (master had 6 commits, #140-147). Both hunks resolved in favour of **master** (newer canonical, to avoid regressing its work):

- **TCS Signals table:** master carries a real S6 improvement (normalize quotes + leading emoji before matching `type:`, so `type: "🔧 Refactor"` resolves to `Refactor`) — strictly better than the branch's older text.
- **⚠️ Post-execution reflect-gate (Phase N) — please confirm:** I took **master's** "HALT + operator runs `/sc:reflect` in a fresh session" design (#142, post-reflect e2e evidence; aligns with `feedback_human_decision_items_must_halt`) over this branch's convergence-era "spawn a subagent, no human session needed" text. I judged master's the newer canonical and the stronger anti-self-rubber-stamp posture — but if the subagent-runs-the-gate approach was a deliberate decision you want to keep, say so and I'll re-resolve that hunk toward the branch.

**Verification:** `tests/skills/test_task_builder_merge.py` 66 passed; `tests/audit/` 1188 passed. Full suite's remaining 17 failures are all the known pre-existing set (`test_install_hooks`, `test_zero_files_analyzed`, `tests/cli/eval/*`, `test_task_id_naming_pattern_preserved`) — none in task-builder/reflect/SKILL. `make verify-sync` + `ruff` clean.

Everything else you restored/decided stays. 🤖
