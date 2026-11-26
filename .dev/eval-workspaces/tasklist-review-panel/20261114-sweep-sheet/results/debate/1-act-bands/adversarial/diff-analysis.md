# Diff Analysis: act-band registration, three position papers

## Metadata
- Generated: 2026-11-15 (orchestrator: claude-sonnet-5-5, no Opus used)
- Variants compared: 3 (V1 haiku defender, V2 sonnet prosecutor, V3 sonnet architect). Files: `variant-1-haiku-defender.md`, `variant-2-sonnet-prosecutor.md`, `variant-3-sonnet-architect.md`
- Mode: B (variants generated from `work/evidence-pack.md`; same agents act as advocates)
- Categories: structural (2), content (7), contradictions (2), unique (4), shared assumptions (4)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Shape of the registration text | one paragraph, numbers unchanged, "unvalidated planning expectations" | decision wording plus a rule paragraph with outcomes inside / overlaps / outside / not assessable | one table row holding numbers, measure, rule, consequence, "may / may not" list | Low |
| S-002 | Where the consequence lives | in prose ("no outside-band result changes gate outcomes") | in a rule sentence under the table | in the row itself, with a copy in `owner-decisions.md` | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Verdict | PASS (bands are non-gating) | FAIL (B-1 to B-4) | FAIL, "narrowly" | High |
| C-002 | Measured quantity (denominator) | keep original definitions, say the two are "not directly comparable" | selection true AND merge_survival true; act true; over selection true and survival not null (so act-and-survive given selected) | selection true, no fallback; survival not counted | High |
| C-003 | Interval rule | none | 90% Wilson; inside / overlaps / outside | 95% Wilson (z 1.96): below / above / not contradicted | Medium |
| C-004 | Minimum data | zero-denominator classes "unestimable" | fewer than 10 item-runs = not assessable | fewer than 10 selected item-runs or fewer than 3 distinct items = not evaluable | Medium |
| C-005 | Consequence of an outside result | nothing; report departure | changes no gate; drops REQ-45 "consistency expected" wording for C4 or C8 | same as V2, plus replace planning value by measured rate; explicit may-not list (no gate, arm, 5.8 action, band move, pooling) | Medium |
| C-006 | Arm and material scope | not stated | SS only | SS only; Stage 1 and Stage 2 reported separately, never pooled; derivation set excluded | Medium |
| C-007 | Pooled band and Z0-anchored band | rejected (pooling hides class split; Z0 band answers a different question) | pooled kept as an optional cross-check; Z0 band impossible before freeze | rejected: mix-dependent; Z0 act is a different quantity and D2 already tests it | Medium |

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact |
|---|---|---|---|---|
| X-001 | Is the act-versus-stage mismatch (F3 versus F4) a blocking defect? | V1: conceded as real but not blocking because no gate or code reads a band | V2/V3: blocking because an outside result is uninterpretable; a selection miss reads as an act miss | High |
| X-002 | Is the missing outside-band consequence blocking? | V1: the documents already imply a non-gating role ("measured rates replace planning probabilities", MR:1102); no registration needed | V2/V3: with nothing registered, the owner picks a reading after seeing data, so the pre-registration is vacuous; REQ-45 wording depends on it | High |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V2 | Worked example of the mismatch: C2 mid 0.325 x s mid 0.55 = 0.18, below the band floor 0.20; C7 0.25 x 0.525 = 0.13, below 0.15 | High |
| U-002 | V2 | `prereg.json` is stamped `owner_confirmed: true` and gates a manual check (`open-manual-checks.sh:8,41`), so the registration is not inert | Medium |
| U-003 | V3 | Rule evaluated by exact arithmetic (`work/v3_rule_sim.py`): flags a correct class at most 0.9%; P(no class flagged) 0.976 at n=10 | High |
| U-004 | V3 | Expected evaluable classes in Stage 2: about 16 selected item-runs for C4, 14 C5, 16 C8, 7-10 for the rest | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact |
|---|---|---|---|---|
| A-001 | No gate, script or report will read a band as a pass/fail test | all three rely on F6 | UNSTATED in the decision text (true of the code today) | High |
| A-002 | Enough selected item-runs per class will exist for a band to be assessed in at least some classes | V2, V3 | UNSTATED, UNVERIFIED (hold-out class mix unknown) | Medium |
| A-003 | A Wilson interval on item-runs is an adequate contradiction test although runs on one item are correlated | V2, V3 | UNSTATED; all figures ignore clustering | Medium |
| A-004 | The act stage of `analyze.py` is the right numerator (supported PROBLEM row, selected item) | V2, V3 | STATED (F4) | Low |

## Summary
- Structural 2, content 7, contradictions 2, unique 4, shared assumptions 4 (UNSTATED 3, STATED 1, CONTRADICTED 0).
- Highest-severity items: C-001, C-002, X-001, X-002.
- Total diff points for convergence: S 2 + C 7 + X 2 + A 4 = 15.
