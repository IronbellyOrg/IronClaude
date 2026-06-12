# REPORT.md template (Wave 5 synthesis skeleton)

## Template overview

Wave 5 reads this ref and emits a `REPORT.md` matching the skeleton below. Every section is fillable without ambiguity: required fields are listed inline, conditional sections name their activation triggers, and worked examples illustrate the exact rendering format. The Grounded vs `[INFERRED]` tag is binary — there is no third bucket. Per-Task Verdicts is conditional and only activates when `per_task_verdicts.length ≥ 2` per §16 row 6 (P4-MANDATORY). The Grounding Gaps section only renders when `grounding-gaps.yaml` is non-empty. All other sections are unconditional.

Wave 5 MUST NOT introduce findings that were not already classified upstream. Unclassifiable findings are dropped before Wave 5 synthesis per §11.1 (no third bucket). Wave 5's job is to render the validated card stream into the skeleton, not to re-judge it.

## Report header (required)

The header block is the first content in the emitted artifact. It is rendered as a fenced YAML block so downstream parsers (sprint TurnLedger, CI) can lift fields without Markdown parsing.

```yaml
contract_version: 1.5.0
status: success | partial | needs_human_decision
mode: pre | post
tier_reached: 1 | 2
confidence_calibrated: 0.00-1.00
citations_total: <int>
citations_revalidated: <int>          # M ≤ citations_total; equals citations_total in full_reread mode
citations_dropped: <int>              # sample-count when sampled; absolute when full_reread
citations_inferred: <int>             # count of [INFERRED]-tagged claims
citation_budget_policy: full_reread | sampled
coverage_degraded: parsed-sparse | null   # D13 Step 1B.2b guard; null when labeling density is healthy (UC-1 only; omit in post mode)
```

Required fields (header is invalid if any are missing):

- `contract_version` — pins the return-contract version this artifact was generated against.
- `status` — terminal verdict. `partial` is forced if evidence-validator dropped any citations, if `--no-evidence-validator` was used, or if `citations_total == 0 AND mode == post` (UC-2 vacuous-success rule, §11.2). UC-1 (`mode == pre`) with `citations_total == 0` is legitimate and may emit `status: success`.
- `mode` — `pre` (UC-1 spec-coverage) or `post` (UC-2 post-execution verdict).
- `tier_reached` — `1` for single-reviewer, `2` for heterogeneous ensemble + adversarial merge.
- `confidence_calibrated` — calibrator-derived score; self-reported confidence is NOT permitted in this field.
- `citations_total / citations_revalidated / citations_dropped / citations_inferred` — see budget-policy band below.
- `citation_budget_policy` — `full_reread` when `citations_total ≤ 20`; `sampled` otherwise.

## Inferred requirements (Pass 2) section (UC-1, D13)

When Step 1B.0 Pass 2 emitted any `INF-NNN` rows, the report includes an `## Inferred requirements (Pass 2)` section rendering one table row per inferred requirement: `| INF id | Verbatim quote | Citation (file:line) | Match result |`. Rows the Wave-5 evidence-validator dropped (quote does not match the cited lines) are listed in a one-line POSTSCRIPT inside this section with the drop reason; dropped INF rows go here and NEVER to the Grounding Gaps section (Grounding Gaps is for report-claim gaps per its own rules). A dropped INF row counts as a dropped citation for the header's `citations_dropped` and therefore forces `status: partial` per the existing dropped-citation rule. The recompute scope is exactly: `coverage_pct_union`, `unmapped_requirements_union`, and `S_dev_density` are recomputed over the surviving union before the report finalizes (the parsed-only `coverage_pct` and `unmapped_requirements` are unaffected by INF drops). When Pass 2 emitted zero rows, the section is omitted entirely (do not emit an empty header). This section is distinct from `[INFERRED]`-tagged report claims below: INF rows are spec-extraction artifacts with load-bearing citations, not non-load-bearing inference chains.

## Grounded vs [INFERRED] tagging conventions

Every claim in the body carries one of exactly two tags (binary, per §11.1):

- **Grounded** — backed by a real `file:line` citation, a real diagnostic command + output, or a real spec/PRD section that survives evidence-validator re-Read. This is the default; un-tagged claims are treated as Grounded.
- **`[INFERRED]`** — a claim the reviewer reached without direct citation. The tag MUST be the literal prefix `[INFERRED]` and MUST appear at the start of the claim line.

There is no third bucket. Findings that the upstream reviewer could not tag either way are dropped before Wave 5 synthesis (per §11.1) and never appear in this template's output. The `[INFERRED]` count surfaces in the header as `citations_inferred: N`.

**WARN trigger.** When `citations_total > 20 AND citations_inferred > citations_total / 2`, Wave 5 surfaces an automatic WARN at the foot of the artifact (see Inferred-claim audit footer below). The artifact still ships; this is a soft signal, not a gate.

## Deviation rendering format

Every deviation is rendered using the block template below. The fields mirror §10.7: file:line, mapped tasklist item, spec section, evidence (verified by evidence-validator), classification rationale (signals matched + gold-standard refs), default remediation, and `[INFERRED]` notes when present.

Per-deviation block template:

```markdown
### Deviation D-<id>: <one-line headline>

- **Location:** <file>:<line>
- **Mapped tasklist item:** <task_id> | unmapped
- **Spec section:** <§N.N title> | n/a
- **Evidence:** <quoted file:line excerpt; verified by evidence-validator>
- **Classification:** <one of: authorized | necessary | drift | regression>
- **Classification rationale:** <signals matched from refs/deviation-taxonomy.md + gold-standard refs cited>
- **Default remediation:** <verb-led action; one sentence>
- **[INFERRED] notes:** <only present when the reviewer attached an inferred sub-claim; prefixed with [INFERRED]>
```

Worked example:

```markdown
### Deviation D-003: Hash algorithm switched without spec authorization

- **Location:** src/superclaude/pm_agent/confidence.py:142
- **Mapped tasklist item:** TASK-PM-20260518-confidence-hash
- **Spec section:** §6.3 Confidence checksum integrity
- **Evidence:** "hashlib.md5(payload).hexdigest()" (src/superclaude/pm_agent/confidence.py:142, re-Read 2026-05-27)
- **Classification:** regression
- **Classification rationale:** Signals matched — security-sensitive hash function downgraded from SHA-256 to MD5; gold-standard ref: refs/deviation-taxonomy.md §3.4 "crypto-downgrade is always regression-class".
- **Default remediation:** Restore SHA-256 in confidence.py:142 and add an integrity regression test under tests/pm_agent/.
- **[INFERRED] notes:** [INFERRED] This may also affect the reflexion checkpoint hash chain — no direct citation, follow-up Read needed.
```

## Grounding Gaps section

When `grounding-gaps.yaml` is non-empty (per §10.6), this section enumerates each row. When the file is empty, the section is omitted entirely (do not emit an empty header).

Section template (one block per gap):

```markdown
## Grounding Gaps

### Gap G-<id>

- **Hunk ref:** <file>:<line-range>
- **Evidence missing:** <what evidence would be needed to classify>
- **Why not classifiable:** <which 4-category signals are absent>
- **Next evidence needed:** <concrete next Read / diagnostic / spec lookup>
```

Each row maps 1:1 to a row in `grounding-gaps.yaml`; Wave 5 does NOT introduce new gaps. If this section is non-empty, the header MUST emit `status: needs_human_decision` (per §10.6).

## Per-Task Verdicts section (P4-MANDATORY when per_task_verdicts.length ≥ 2)

**Activation rule.** This section is emitted if and only if the return contract's `per_task_verdicts` array has length ≥ 2 (§16 row 6, P4-MANDATORY). When length is 0 or 1, the section is omitted entirely. The verdicts are lifted directly from the contract array; Wave 5 does not recompute them.

Per-task subsection template:

```markdown
### Task <task_id>

- **Status:** success | partial | regression
- **Deviation class:** authorized | necessary | drift | regression | none
- **Citations dropped:** <int>
- **Per-task validation strength:** strong | weak | none
- **Evidence anchor:** <file>:<line> | (no evidence anchor)
```

Worked example (2 tasks, demonstrating the activation case):

```markdown
## Per-Task Verdicts

### Task TASK-PM-20260518-confidence-hash

- **Status:** regression
- **Deviation class:** regression
- **Citations dropped:** 0
- **Per-task validation strength:** strong
- **Evidence anchor:** src/superclaude/pm_agent/confidence.py:142

### Task TASK-PM-20260519-reflexion-checkpoint

- **Status:** success
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** strong
- **Evidence anchor:** src/superclaude/pm_agent/reflexion.py:88
```

## Budget-policy reporting band

When `citation_budget_policy: sampled`, Wave 5 emits this band immediately below the header. When `citation_budget_policy: full_reread`, the band is omitted (the header alone is sufficient).

Band template:

```markdown
> **Citation budget: sampled mode**
> - `citations_revalidated: M` — size of the re-Read sample (M ≤ citations_total).
> - `citations_dropped: <sample-count>` — drops observed in the sample only. This is the field that gates promotion (§14.5.2 condition 6a strict `== 0` check).
> - `citations_dropped_extrapolated: <projection>` — population-level estimate, `round(citations_dropped × (citations_total / citations_revalidated))`. Recording-only; does not gate promotion. A non-zero value SHOULD prompt a follow-up `--depth deep` run that forces `full_reread`.
```

Interpretation hint (rendered as the last line of the band): "The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read."

## Inferred-claim audit footer

Rendered as the final section before Recommendations. Always surfaces `citations_inferred: N` even when N = 0 (so operators can confirm the audit ran).

Footer template:

```markdown
## Inferred-claim audit

- `citations_inferred: <int>`
- Inferred-fraction: `<citations_inferred> / <citations_total>` = <float, 2 dp>

<!-- WARN block — only rendered when citations_total > 20 AND citations_inferred > citations_total / 2 -->
> **WARN:** Reflection is more inference than evidence. Consider re-running with `--depth deep` or providing more grounding artifacts.
```

The WARN block activates only when both conditions are true: `citations_total > 20` AND `citations_inferred > citations_total / 2`. Below the >20 threshold, low absolute citation counts can legitimately skew the ratio without indicating a problem.

## Recommendations section

Per §12.1 dimension #4 ("Recommendation actionability"), every recommendation MUST be actionable: it names the file, the change, and the verifier that confirms the change landed. Vague advice ("consider improving error handling") is NOT permitted in this section and will be down-graded by the grader.

Section template (one block per recommendation):

```markdown
## Recommendations

### Recommendation R-<id>: <verb-led headline>

- **File:** <path> (or "n/a" for cross-cutting recs with no single file target)
- **Change:** <one-sentence description of the modification>
- **Verifier:** <test command, diagnostic Read, or spec-section re-check that confirms the change>
- **Linked deviation(s):** D-<id>[, D-<id>...] | none (for proactive recs)
- **Priority:** P0 | P1 | P2
```

Worked example:

```markdown
### Recommendation R-001: Restore SHA-256 in confidence checksum

- **File:** src/superclaude/pm_agent/confidence.py
- **Change:** Replace `hashlib.md5` at line 142 with `hashlib.sha256` and update the checksum width in the schema test.
- **Verifier:** `uv run pytest tests/pm_agent/test_confidence_checksum.py -v` passes; re-Read confidence.py:142 confirms SHA-256.
- **Linked deviation(s):** D-003
- **Priority:** P0
```

Wave 5 ordering: P0 recommendations first, then P1, then P2. Within a priority, deviation-linked recs precede proactive recs. Cross-cutting recs (no `file` target) appear last in their priority band.
