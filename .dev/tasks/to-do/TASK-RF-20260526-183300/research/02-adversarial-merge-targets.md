# Adversarial Merge Targets Research

Status: Complete

## Scope and Sources Read

- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md`

## Findings: Exact Change Targets

### 1. Requirement-level provenance

Current provenance requirements are section/block-level, not requirement-level:

- Debate protocol Step 5 says to add provenance annotations as "source attribution per merged section" at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:253-254`.
- The provenance format examples identify variant and section only at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:260-266`.
- Artifact template rules require every "section or significant block" to include a source tag, with variant, section reference, and change number if applicable, at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:349-377`.

Exact change targets:

1. In `debate-protocol.md`, expand Step 5 process item 4 at lines 253-254 from section-level source attribution to requirement-level provenance when merging requirement-bearing artifacts.
2. In `debate-protocol.md`, expand the "Provenance Annotation Format" block at lines 260-266 with requirement IDs / requirement anchors, e.g. source requirement, target requirement, merge change, and decision basis.
3. In `artifact-templates.md`, expand Section 6 heading/rules at lines 349-377 to require provenance for each requirement, acceptance criterion, constraint, risk, and other requirement-level anchor, not just every section or significant block.
4. In `artifact-templates.md`, add requirement-level provenance fields to the merged output example at lines 353-368.

### 2. Concrete-over-generic merge rule

Current merge planning/execution does not define a precedence rule for preserving concrete content over generic summaries:

- Step 4 only says to incorporate non-base strengths with source, target, rationale, integration approach, and risk level at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:207-216`.
- Step 5 only says to apply planned changes, maintain structural integrity, and validate the result at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:248-258`.
- The refactor-plan template's planned-change fields do not include a specificity/concreteness preservation check at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:249-264`.
- The merge-log template records before/after summaries and validation but has no field showing whether concrete anchors were preserved at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:301-320`.

Exact change targets:

1. In `debate-protocol.md`, add a Step 4 planning rule after lines 207-216: when source and target express the same requirement/constraint, preserve the more concrete version unless contradicted by a higher-confidence debate finding.
2. In `debate-protocol.md`, add a Step 5 execution rule after lines 250-254: do not replace specific IDs, thresholds, constraints, examples, acceptance criteria, or implementation anchors with generic prose during merge.
3. In `artifact-templates.md`, add a planned-change field after line 256 such as `- **Concrete anchors preserved**: <IDs/thresholds/constraints/examples retained or rationale if changed>`.
4. In `artifact-templates.md`, add a merge-log field after line 309 or 318 recording concrete anchors preserved/dropped for each applied change.

### 3. Threshold preservation

Current templates capture convergence threshold and score margin, but not preservation of source requirements' own thresholds during merge:

- Debate convergence threshold is configurable and recorded in `debate-protocol.md` at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:147-158`.
- The debate transcript template records convergence threshold at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:71-76` and again in the convergence assessment at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:141-146`.
- Base selection records a 5% margin threshold at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:212-220`.
- Merge execution validation currently checks structure, references, and contradictions only at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:253-258` and `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:323-338`.

Exact change targets:

1. In `debate-protocol.md`, add threshold-preservation to Step 4's integration plan structure after lines 211-215: every numeric threshold/limit/SLO/percentage/count inherited from any variant must be listed with source and target disposition.
2. In `debate-protocol.md`, add threshold-preservation to Step 5 validation after lines 254-258: verify thresholds from accepted changes are preserved exactly unless the merge log gives an explicit rationale.
3. In `artifact-templates.md`, add a `## Threshold Preservation` table to `refactor-plan.md` after planned changes and before "Changes NOT Being Made" at lines 249-267.
4. In `artifact-templates.md`, add a `### Threshold Preservation` subsection to post-merge validation after lines 323-338, with counts for preserved, modified-with-rationale, and dropped-with-rationale thresholds.

### 4. Dropped-anchor rationale

Current protocol requires rationale for changes not being made, but only at the diff-point/non-base approach level; it does not require rationale for specific anchors dropped during accepted merges:

- Step 4 says "Changes NOT being made" should include differences where the base approach was superior at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:223-226`.
- The refactor-plan template has a "Changes NOT Being Made" table with `Diff Point`, `Non-Base Approach`, and `Rationale for Keeping Base` at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:267-272`.
- The merge-log template allows `Skipped` status and final skipped counts/reasons at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:303-320` and `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:339-344`.
- No current field identifies dropped anchors such as requirement IDs, acceptance criteria, thresholds, dependencies, examples, or references inside a change that was otherwise applied.

Exact change targets:

1. In `debate-protocol.md`, expand Step 4 "Changes NOT being made" at lines 223-226 into an anchor-level rule: every omitted requirement-level anchor from a non-base variant must be listed with source, reason, and evidence.
2. In `debate-protocol.md`, add a Step 5 merge-log requirement near line 258: if execution drops or rewrites a source anchor, record the anchor ID/text, decision basis, and replacement target if any.
3. In `artifact-templates.md`, extend the refactor-plan "Changes NOT Being Made" table at lines 267-272 with columns for `Dropped Anchor(s)`, `Anchor Type`, and `Evidence/Rationale`.
4. In `artifact-templates.md`, add a per-change merge-log field after lines 303-310 and 312-319: `- **Dropped anchors**: <none | list with rationale>`.
5. In `artifact-templates.md`, add a post-merge validation subsection after lines 323-338: `### Dropped Anchor Audit` with totals and required rationale coverage.

### 5. Merged output templates

The current merged output template is provenance-oriented but not requirement-audit-oriented:

- Section 6 states the merged output includes inline provenance annotations at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:349-352`.
- The example header includes only provenance, base, and merge date at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:353-357`.
- Example source tags show base original, incorporated variant content, and modified base content at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:360-367`.
- Provenance rules identify variant/section/change number but not requirement IDs, threshold state, or dropped anchors at `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:370-377`.

Exact change targets:

1. Rename or expand `artifact-templates.md` Section 6 at lines 349-377 from "Merged Output Provenance Format" to a merged output template that includes a header, provenance tags, requirement-level anchor tags, threshold audit, and dropped-anchor audit.
2. Add a metadata header field after lines 353-357 for source variant count, selected base, refactor-plan ID/path, merge-log path, and validation status.
3. Add inline requirement-anchor examples after lines 360-367, e.g. tags that include `Requirement`, `Source`, `Change`, `Thresholds`, and `Disposition`.
4. Add a required end-of-document audit block after line 368 listing preserved anchors, modified anchors with rationale, dropped anchors with rationale, and unresolved references.
5. Add rules after lines 370-377 stating that merged output must not omit an accepted requirement-level anchor without a local tag and a matching merge-log entry.

## Summary

Recommended change areas are concentrated in two files:

1. `debate-protocol.md` Step 4 and Step 5 should gain normative merge rules for requirement-level provenance, concrete-over-generic precedence, threshold preservation, and dropped-anchor rationale.
2. `artifact-templates.md` Section 4 (`refactor-plan.md`), Section 5 (`merge-log.md`), and Section 6 (`Merged Output Provenance Format`) should gain concrete fields/tables so the protocol can enforce those rules in generated artifacts.

No unverified findings are included; all claims above are grounded in the two assigned files only.

Status: Complete
