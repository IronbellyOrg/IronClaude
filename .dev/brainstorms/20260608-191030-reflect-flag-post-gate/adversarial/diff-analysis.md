# Diff Analysis: `--reflect auto|1|2` spec comparison

## Metadata
- Generated: 2026-06-08T19:35:00Z
- Variants compared: 3 (V1 opus:architect, V2 opus:refactorer, V3 haiku:qa)
- Total differences found: 17 (structural 3, content 6, contradictions 3, unique 3, shared assumptions 2)
- Depth: deep | Convergence threshold: 0.75

## Structural Differences

| # | Area | V1 architect | V2 refactorer | V3 qa | Severity |
|---|---|---|---|---|---|
| S-001 | Section layout | 12 sections, dial-centric (§4 FER, §5 reconciliation) | 12 sections + inline diffs | 13 sections + §13 Acceptance Test Matrix | Low |
| S-002 | Template presentation | full literal blocks | **unified diff vs current :1994–1999** | literal blocks + per-template AT | Medium |
| S-003 | Validation presentation | prose rewrite of :2051/:2108 + 1 rf-qa invariant | 2 diff edits A/B + 1 rf-qa MODE-MATCH | **exhaustive V1–V16 table + mode→assertion map** | Medium |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Legacy `POST_REFLECT_MODE: halt` mapping | retained `halt` position → byte-identical manual item | `halt → Mode 1` (inline); `none`/`DISABLED` = byte-identical | `halt → 2` | **High** |
| C-002 | `auto` predicate | `W=false→1` then `S6∨S5∨TCS≥35`, then `S2≥3→2` in standard band | `S6==1 ∨ S5>0 ∨ TCS≥35 → 2` | `TCS≥35 ∨ S6==1 → 2` (no S5) | **High** |
| C-003 | Mode-1 subagent-executor detection | runtime self-check in emitted item (HALT if subagent) | runtime self-check (HALT `mode1-needs-top-level-executor`) | build-time `agent_tool_depth>0` → degrade to HALT | Medium |
| C-004 | BUILD_REQUEST field name | `REFLECT:` | `REFLECT_POST:` | `REFLECT_POST_MODE:` | Low |
| C-005 | `auto`+wrapper-absent | Gate-0 unconditionally → Mode 1 | (no explicit auto-absent case) | degrade to manual (same as fixed-2) | Medium |
| C-006 | Depth source for retained manual/`halt` | `max(TCS-band, standard)` (existing) | disabled item keeps `--depth {DEPTH}` (TCS O4-floored) | Mode 2 passthrough; manual keeps TCS depth | Low |

## Contradictions

| # | Point of conflict | Positions | Impact |
|---|---|---|---|
| X-001 | What `none`/`DISABLED` emits | V1/V3: **no item** (gate off). V2: **the manual HALT item** ("zero delta" for DISABLED) | **High** — V2 contradicts today's behavior (today `DISABLED` ⇒ no POST item; the manual item is the `ENABLED` shape). Conflates "no gate" with "manual gate". |
| X-002 | Is `halt` a distinct state from `none`? | V1: yes (`none`=no item, `halt`=manual item present). V2: no (collapses). V3: no (`halt→2`) | Medium — resolved by adopting V1's distinction; it is exactly what the wrapper-absent fallback needs. |
| X-003 | Does fixed `--reflect 1` need a guard on high-risk tasklists? | V1/V2/V3: silent (operator authority) | Medium — surfaced as INV finding; advisory warning recommended. |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V3 | Exhaustive V1–V16 validation assertion matrix + per-mode active-assertion map + §13 FR→test matrix | **High** |
| U-002 | V2 | Unified-diff presentation of the Mode-2 template against current :1994–1999 (implementer-friendly) + executor-disjointness trade-off table | High |
| U-003 | V1 | Distinct `none` vs `halt` ordinal model + single-producer FR-9 invariant + the asymmetric-fallback rationale | High |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Status |
|---|---|---|---|---|
| A-001 | The `superclaude reflect run` wrapper (sibling spec) is the Mode-2 target and is OUT of scope to build/modify | all 3 | STATED | accepted |
| A-002 | The builder cannot reliably know at build time whether the future `/task` executor will be a subagent | implicit in V1/V2 (runtime check); **CONTRADICTED by V3** (build-time `agent_tool_depth`) | UNSTATED→promoted | debate: resolved to runtime-primary |

## Summary
- Highest-severity items: X-001 (none semantics), C-001 (halt mapping), C-002 (auto predicate)
- All three converge on: one unified dial; TCS+S6-based auto; Mode-1 inline-standard-audit-only; Mode-2 Bash-shell-out-deep-remediate; O4 preserved-by-construction; every item HALTs + writes `reflect_post`; wrapper-absent → manual (not Mode 1); `reflect_post_mode` frontmatter oracle; mode-aware validation.
