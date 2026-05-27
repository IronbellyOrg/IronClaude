# Change F Follow-Up — SKILL.md L340 Audit-Log Enum Alignment

**Source of finding:** `phase-outputs/reviews/skill-md-dispatch-verdict.md` § L340 section
**Identified during:** Change C / Track 2 / Step 4.2

## (1) Title

Align SKILL.md L340 audit-log `escalation_reason` enumeration with rubric

## (2) Why

The `<!-- SC:TROUBLESHOOT:SUMMARY ... -->` audit-log footer at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:340` currently lists 5 allowed `escalation_reason` values, but the rubric (`refs/escalation-rubric.md`) defines 7 values pre-Change-C and 8 values post-Change-C:

- **Currently listed (5):** `none`, `low_confidence`, `multi_domain`, `forced_by_depth_deep`, `intermittent`
- **Missing pre-existing (2 — pre-Change-C tech debt):** `not_reproducible` (rubric § Escalation Decision rule 3), `security_caution` (rubric § Escalation Decision rule 3)
- **Missing new (1 — added by Change A, consumed by Change C):** `source_only_dynamic_claim` (rubric § Escalation Decision rule 3)

Change C extends the calibrator to be able to RETURN `source_only_dynamic_claim` (calibrator Responsibilities #6, post-edit file L63). The audit log enumeration in SKILL.md is now out of sync by 3 values total, where Change C contributes 1 of the 3.

## (3) Scope

Edit `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:340` to extend the enumeration. Proposed replacement:

**Old (verbatim L340):**

```
escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>
```

**New (proposed):**

```
escalation_reason: <none|low_confidence|multi_domain|not_reproducible|forced_by_depth_deep|intermittent|security_caution|source_only_dynamic_claim>
```

8 values total, matching the rubric.

## (4) Out-of-scope reason for Change C

Change C's scope is the calibrator agent prompt ONLY (`src/superclaude/agents/confidence-calibrator.md`). SKILL.md is the dispatcher (not the agent) and is owned by Change F (the final integration step in the A→B→C→F→E sequenced rollout). Modifying SKILL.md inside Change C would expand the blast radius and violate the per-change scoping discipline of the cross-env proposal.

Additionally, the `not_reproducible` and `security_caution` gaps are pre-existing tech debt (predate this PR series) — Change C only adds `source_only_dynamic_claim`. Bundling all three fixes into a single Change F edit is cleaner than splitting them.

## (5) Verbatim quote of the current L340 line

From `phase-outputs/reviews/skill-md-dispatch-verdict.md` § L340 section:

> escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>

(5 values; literal `<` and `>` delimiters; pipe-separated.)

## Related bundle: SKILL.md L199 staleness

The "5-dimension rubric" phrase on SKILL.md L199 is also stale post-Change-A/C (now 6 dimensions). Already flagged in this task's frontmatter Risks section as a follow-up bundled with this Change F entry. The two SKILL.md staleness items together form the Change F SKILL.md cleanup scope:

1. L199: `5-dimension rubric` → `6-dimension rubric`
2. L340: extend `escalation_reason` enumeration from 5 → 8 values

Both edits should land in the same Change F commit.
