<!-- markdownlint-disable MD024 -->
<!-- MD024 disabled: each of the 5 Steps reuses ### Purpose / ### Input / ### Process / ### Output / ### Delegation subsection headings by design. -->

# Debate Protocol Reference

Detailed protocol specification for the 5-step adversarial debate pipeline.

## Protocol Overview

The adversarial pipeline executes 5 sequential steps, each producing a
documented artifact. Steps must execute in order — each step's output feeds
into the next.

```text
Step 1: Diff Analysis → diff-analysis.md
Step 2: Adversarial Debate → debate-transcript.md
Step 3: Base Selection → base-selection.md
Step 4: Refactoring Plan → refactor-plan.md
Step 5: Merge Execution → merge-log.md + merged output
```

---

## Step 1: Diff Analysis

### Purpose

Systematic comparison identifying structural differences, content differences, contradictions, and unique contributions across all variants.

### Input

- All variant artifacts (2-10 files)

### Process

#### 1.1 Structural Diff

Compare section ordering, hierarchy depth, and heading structure across variants.

```yaml
structural_comparison:
  section_ordering: "Compare top-level section sequence across variants"
  hierarchy_depth: "Measure max nesting level per variant"
  heading_structure: "Map heading types and counts"
  severity_rating:
    Low: "Cosmetic differences (ordering preference)"
    Medium: "Structural approaches differ meaningfully"
    High: "Incompatible organizational models"
```

#### 1.2 Content Diff

Compare approaches topic-by-topic, identifying coverage differences.

```yaml
content_comparison:
  topic_extraction: "Identify topics addressed by each variant"
  approach_comparison: "For shared topics, describe each variant's approach"
  coverage_gaps: "Topics covered by some variants but not others"
  detail_level: "Compare depth of coverage per topic"
```

#### 1.3 Contradiction Detection

A contradiction is identified when:

1. Two statements within the same variant make opposing claims about the same subject
2. A stated requirement conflicts with a stated constraint
3. A timeline or dependency creates an impossible sequence

**Structured scan protocol**:

- For each claim in each variant, check whether any other claim asserts the opposite or an incompatible position
- Claims must be specific enough to be falsifiable — vague statements cannot contradict
- Cross-variant contradictions are categorized separately from intra-variant contradictions

#### 1.4 Unique Contribution Extraction

Identify ideas present in only one variant with value assessment.

```yaml
unique_contributions:
  detection: "Ideas/sections/approaches present in exactly one variant"
  value_assessment:
    High: "Addresses a gap no other variant covers; high impact"
    Medium: "Useful addition but not critical"
    Low: "Nice to have, minimal impact"
```

### Output

`diff-analysis.md` — organized by category (structural, content, contradictions, unique) with severity ratings and variant attribution.

### Delegation

Analytical agent or `/sc:analyze` equivalent.

---

## Step 2: Adversarial Debate

### Purpose

Structured debate where agents argue for their variant's approach, using steelman strategy.

### Input

- All variants + diff-analysis.md

### Steelman Requirement

Advocates MUST construct the strongest possible version of opposing positions
before critiquing them. This is not a zero-sum competition — the goal is to
identify genuine strengths from all sides.

### Round Structure

#### Round 1: Advocate Statements (Parallel)

- Each variant gets one advocate agent
- Advocate receives: their variant + all other variants + diff-analysis.md
- Advocate produces:
  - Summary of their position
  - Key strengths claimed (with evidence from their variant)
  - Steelman of each opposing variant's strongest points
  - Weaknesses identified in other variants (with evidence)
- **Execution**: All advocates run in parallel via Task tool

#### Round 2: Rebuttals (Sequential)

- **Condition**: `--depth standard` or `--depth deep`
- Each advocate receives all Round 1 transcripts
- Advocate produces:
  - Response to criticisms of their variant
  - Counter-evidence or concessions where criticism is valid
  - Updated assessment of other variants based on their defenses
- **Execution**: Sequential — each advocate sees all previous rebuttals

#### Round 3: Final Arguments (Conditional)

- **Condition**: `--depth deep` AND convergence < threshold
- Final positions after considering all rebuttals
- Focus on remaining unresolved disagreements
- **Execution**: Sequential

### Depth Control

| Depth | Rounds | Convergence Check |
|-------|--------|-------------------|
| quick | 1 (advocate only) | No convergence check |
| standard | 2 (advocate + rebuttal) | Post-Round 2 convergence check |
| deep | Up to 3 | Convergence checked after each round; stop if threshold met |

### Convergence Detection

```yaml
convergence:
  metric: "Percentage of diff points where agents agree on superior approach"
  threshold: "Configurable via --convergence flag (default 0.80)"
  calculation: "agreed_points / total_diff_points"
  tracking: "Per-point agreement updated after each round"
  status:
    CONVERGED: "Agreement >= threshold"
    NOT_CONVERGED: "Agreement < threshold after max rounds"
```

### Per-Point Scoring Matrix

For each diff point from Step 1:

- **Winner**: Which variant's approach is superior for this point
- **Confidence**: Percentage confidence in the winner assessment
- **Evidence summary**: Key evidence supporting the winner determination

### Output

`debate-transcript.md` — full debate with per-point scoring matrix and convergence assessment.

### Delegation

debate-orchestrator coordinates; domain agents participate as advocates.

---

## Step 3: Base Selection

See `scoring-protocol.md` for the complete hybrid quantitative-qualitative scoring algorithm.

### Summary

- Quantitative layer (50%): 5 deterministic metrics
- Qualitative layer (50%): 25-criterion additive binary rubric with CEV protocol
- Position-bias mitigation: Forward + reverse evaluation order
- Tiebreaker: Debate performance → correctness count → input order

### Output

`base-selection.md` — full scoring breakdown with evidence citations and selection rationale.

---

## Step 4: Refactoring Plan

### Purpose

Generate actionable plan to incorporate strengths from non-base variants into the selected base.

### Input

- Selected base variant
- All non-base variants
- debate-transcript.md (for evidence of which approaches were determined superior)

### Plan Structure

For each non-base strength (as determined by debate):

1. **Source**: Which variant and section contains the strength
2. **Target**: Where it integrates into the base
3. **Rationale**: Debate evidence supporting incorporation
4. **Integration approach**: How to merge (replace, append, insert, restructure)
5. **Risk level**: Low (additive), Medium (modifies existing), High (restructures)
6. **Concrete anchors preserved**: List the requirement IDs, thresholds,
   constraints, acceptance criteria, examples, and implementation anchors
   carried over verbatim from the source — or, if any are intentionally
   modified, record the rationale here. Anchor categories include: requirement
   IDs (FR-/NFR-/AC-), numeric thresholds/SLOs/percentages/counts, named
   systems/files/endpoints/components, dates/deadlines, stakeholder
   constraints, rollback bounds, compliance/audit requirements.
7. **Threshold preservation**: Every numeric threshold, limit, SLO, percentage,
   or count inherited from any variant MUST be listed with `source variant`,
   `value`, and `target disposition` (preserved-exact / modified-with-rationale
   / dropped-with-rationale). A planned change that touches a section
   containing thresholds without listing them here is a planning gap and MUST
   be returned to Step 4 before merge.

#### Concrete-over-generic precedence rule (Step 4 planning)

When source and target express the same requirement, constraint, acceptance
criterion, or implementation anchor, the merge plan MUST preserve the more
concrete version unless a higher-confidence debate finding explicitly
contradicts the concrete content. "More concrete" means: contains specific IDs,
numeric thresholds, named systems/files/endpoints/dates, or worked examples
rather than generic taxonomy, prose, or governance categories. Governance,
safety, lifecycle, policy-first, and proof-gate additions from non-base
variants are AUGMENTATION — they wrap or extend concrete anchors but MUST NOT
replace them with a higher-level summary.

For each base weakness identified during debate:

1. **Issue**: What was identified as weak
2. **Better variant**: Which non-base variant addresses it
3. **Fix approach**: How to address the weakness

Changes NOT being made (with rationale):

- Differences where the base approach was determined superior in debate
- **Anchor-level rule**: For every non-base variant, list each omitted
  requirement-level anchor (requirement ID, acceptance criterion, threshold,
  named system, dependency, example, or compliance reference) with
  `source variant`, `anchor type`, `anchor text or ID`, `reason for omission`,
  and `evidence from debate transcript`. A non-base variant's anchor MAY NOT be
  silently dropped — either it is preserved in the merged output, replaced
  with a documented equivalent, or listed here with rationale.

### Review

- Default: Auto-approved
- Interactive mode: User approval required before Step 5

### Output

`refactor-plan.md` — actionable merge plan with integration points.

---

## Step 5: Merge Execution

### Purpose

Execute the refactoring plan to produce a unified output.

### Input

- Base variant + refactor-plan.md

### Process

1. Read base variant and plan
2. Apply each planned change methodically (in plan order)
3. Maintain structural integrity (heading hierarchy, section flow)
4. Add provenance annotations at the requirement level when the merged
   artifact contains requirement-bearing content (requirements, acceptance
   criteria, constraints, risks, thresholds, named systems). Section-level
   attribution alone is INSUFFICIENT for requirement-bearing artifacts — every
   requirement, acceptance criterion, constraint, risk entry, and explicit
   threshold MUST carry an inline provenance tag identifying source variant,
   source requirement ID/anchor, target ID/anchor, and the refactor-plan
   change number when applicable. Non-requirement-bearing artifacts (e.g.
   narrative documents) may use section-level provenance.
5. **Concrete-over-generic execution rule**: When applying a planned change,
   DO NOT replace specific requirement IDs, numeric thresholds, constraints,
   named systems/files/endpoints, dates/deadlines, worked examples, acceptance
   criteria, or implementation anchors with generic taxonomy or governance
   prose. If a planned change appears to drop or paraphrase such anchors, halt
   execution of that change, record a deviation in the merge log, and either
   (a) re-plan with the anchor preserved, or (b) return the unresolved anchor
   to Step 4 for re-evaluation. Governance, safety, lifecycle, policy, and
   proof-gate additions are merged as augmentation around concrete content,
   not as replacements for it.
6. **Dropped-anchor merge-log entry**: If execution drops, paraphrases, or
   rewrites a source anchor (requirement ID, acceptance criterion, threshold,
   named system, dependency, example, compliance reference), the merge log
   MUST record `anchor ID or verbatim text`, `source variant`, `change
   number`, `decision basis`, and `replacement target if any`. An anchor that
   appears in any variant's accepted content but is absent from the merged
   output without a matching merge-log entry is a merge-execution failure and
   MUST be flagged in post-merge validation.
7. Post-merge validation:
   - Structural integrity check
   - Internal reference validation
   - Contradiction re-scan
   - **Threshold preservation check**: Verify that every numeric threshold,
     limit, SLO, percentage, or count listed in the Step 4
     threshold-preservation table is present in the merged output with its
     exact value, OR has a merge-log entry recording the change with
     rationale. Modified or dropped thresholds without a documented rationale
     FAIL this gate.
   - **Dropped-anchor audit**: Compare the set of accepted requirement-level
     anchors in the refactor plan against anchors present in the merged
     output. Every accepted anchor MUST either appear in the merged output
     with an inline requirement-level provenance tag, OR carry a merge-log
     entry per item 6. Unaccounted-for accepted anchors FAIL this gate.
8. Produce merge-log.md

### Provenance Annotation Format

For section-level attribution (non-requirement-bearing content):

```markdown
<!-- Source: Variant A (opus:architect), Section 3.2 -->
<!-- Source: Variant B (sonnet:security), Section 4.1 — merged per refactor-plan Change #3 -->
<!-- Source: Base (original) -->
```

For requirement-level attribution (requirements, acceptance criteria, constraints, risks, thresholds — REQUIRED for requirement-bearing artifacts):

```markdown
<!-- Source: Variant A (opus:architect), Requirement FR-007 → Target FR-012, Change #4, Disposition: preserved-exact -->
<!-- Source: Variant B (sonnet:security), AC-NFR-3 → Target AC-NFR-5, Change #7, Disposition: modified, Decision basis: debate consensus on threshold harmonization -->
<!-- Source: Variant C (sonnet:performance), Threshold "p95 < 300ms" → Target NFR-Perf-2, Change #9, Disposition: preserved-exact -->
<!-- Source: Base (original), Requirement FR-001, Disposition: preserved-exact -->
```

Each requirement-level tag MUST include: `Source variant`, `Source requirement
ID or anchor`, `Target ID or anchor`, `Change #` (linking to the refactor
plan), and `Disposition` (preserved-exact / modified / merged-from-multiple).
Tags for modified or merged anchors MUST include `Decision basis`.

### Output

- Unified merged artifact
- `merge-log.md` — per-change execution log

### Delegation

merge-executor agent (dedicated specialist).

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Agent fails to generate variant | Retry once, then proceed with N-1 variants (min 2) |
| Variants too similar (<10% diff) | Skip debate, select either, log "substantially identical" |
| No convergence after max rounds | Force-select by score, document non-convergence |
| Merge produces invalid output | Preserve all artifacts, flag failure, provide plan for manual execution |
| Single variant remains | Abort adversarial, return surviving variant with warning |

---

*Reference document for sc:adversarial skill*
*Source: SC-ADVERSARIAL-SPEC.md FR-002, FR-006*
