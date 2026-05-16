# Research: Data Models — 5 PRD §25 Schemas

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Data Model Analyst
**Source:** PRD §25 + current SKILL.md schema verification

---

## 1. §25.1 Execution Context Header (FR-CONV.2 output)

**Source:** PRD `PRD_TASK_BUILDER_CONVERGENCE.md:944-954`

### Verbatim YAML schema

```yaml
"## Execution Context":
  References:        # list of BUILD_REQUEST refs (GOAL, WHY, related-doc IDs)
    - "R-###: <ref-line>"
  Source areas:      # list of named modules/packages — NEVER specific file paths
    - "<package-or-module-name>"
  Key constraints:   # top 1-3 invariants from BUILD_REQUEST
    - "<invariant statement>"
```

### Per-field table

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `References` | list[string] | Yes | BUILD_REQUEST refs (GOAL, WHY, related-doc IDs) | Each item formatted `"R-###: <ref-line>"` (PRD:948-949) |
| `Source areas` | list[string] | Yes | Named modules/packages | **NEVER specific file paths** — hidden-input determinism rule (PRD:950-951) |
| `Key constraints` | list[string] | Yes (1-3 items) | Top invariants from BUILD_REQUEST | Bounded 1-3 entries per PRD:952 inline comment |

### Block-level constraint

When BUILD_REQUEST is minimal, the block **degrades to References-only** (omit `Source areas` and `Key constraints` when not derivable). This degradation rule is asserted in PRD FR-CONV.2 (cross-section dependency); the §25.1 schema itself is the maximal form.

---

## 2. §25.2 Inherited Structural Verdict Block (FR-CONV.3 output)

**Source:** PRD `PRD_TASK_BUILDER_CONVERGENCE.md:956-963`

### Verbatim YAML schema

```yaml
"## Inherited Structural Verdict":
  rf_qa_table_verbatim: <copy of rf-qa task-integrity table at spawn time>
  prompt_directive: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."
  reinjection_rule: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."
```

### Per-field table

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `rf_qa_table_verbatim` | string / markdown block | Yes | Verbatim copy of rf-qa task-integrity verdict table at spawn time | No editing, no summarization — byte-exact copy (PRD:960) |
| `prompt_directive` | string | Yes | Directive to rf-qa-qualitative on how to use the verdict | **Fixed value** (PRD:961): `"PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."` |
| `reinjection_rule` | string | Yes | Freshness rule | **Fixed value** (PRD:962): `"On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."` |

---

## 3. §25.3 Synthetic DNSP Finding (FR-CONV.6 output)

**Source:** PRD `PRD_TASK_BUILDER_CONVERGENCE.md:965-976`

### Verbatim YAML schema

```yaml
synthetic_dnsp_finding:
  severity: HIGH                                # fixed
  source: "synthetic-dnsp"                      # fixed
  affected_range: "<agent's assigned_files slice>"
  evidence: "<spawn-log path, OR stub citing log absence>"
  recommendation: "Manual review required — partition agent failed twice"
  dedup_key: "(assigned_files_range, escalation_ladder_exhaust_point)"
  found_n_times: <int, default 1>               # increments on dedup collapse
```

### Per-field table

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `severity` | enum | Yes | DNSP severity level | **Fixed = `HIGH`** (PRD:969) |
| `source` | string | Yes | Origin tag for finding | **Fixed = `"synthetic-dnsp"`** (PRD:970) |
| `affected_range` | string | Yes | Agent's assigned_files slice | Free-form range descriptor (PRD:971) |
| `evidence` | string | Yes | Spawn-log path OR stub citing log absence | If log missing, stub must explicitly cite absence (PRD:972) |
| `recommendation` | string | Yes | Action to operator | **Fixed value** (PRD:973): `"Manual review required — partition agent failed twice"` |
| `dedup_key` | tuple | Yes | Identity for dedup-collapse | Composite: `(assigned_files_range, escalation_ladder_exhaust_point)` (PRD:974) |
| `found_n_times` | int | Yes | Collision counter | Default `1`; **increments on dedup collapse** (PRD:975) |

---

## 4. §25.4 Per-Item Checklist Schema (NFR-CONV.6 operational source)

**Source:** PRD `PRD_TASK_BUILDER_CONVERGENCE.md:978-987`

### Verbatim YAML schema

```yaml
per_item_schema:
  Description: "<one-line task-item action statement>"
  Context: "<file:line citation OR justified-absence comment>"     # TB-Add-8 enforced
  Acceptance: "<observable success condition>"
  Confidence: "<HIGH|MEDIUM|LOW> — with one-line rationale"
  Verification: "<command, file inspection, or test to confirm Acceptance>"
```

### Per-field table

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `Description` | string | Yes | One-line task-item action statement | Single line; imperative voice (PRD:982) |
| `Context` | string | Yes | `file:line` citation OR justified-absence comment | **TB-Add-8 enforced** (PRD:983) — when no citation available, must be justified-absence comment, not empty |
| `Acceptance` | string | Yes | Observable success condition | Must be observable (verifiable from outside) (PRD:984) |
| `Confidence` | enum {HIGH, MEDIUM, LOW} | Yes | Confidence with rationale | Must include one-line rationale alongside the enum value (PRD:985) |
| `Verification` | string | Yes | Command, file inspection, or test to confirm Acceptance | Concrete and executable; pairs with `Acceptance` (PRD:986) |

### Cross-reference with current SKILL.md

**Comparison target:** `src/superclaude/skills/task-builder/SKILL.md:1450-1460`

The lines SKILL.md:1450-1460 do **not** contain the §25.4 per-item 5-field schema. They contain a different "phase template" with fields **{Context, Action, Output, Verification, Completion gate}**:

```
## Phase 1: [Phase Name]

- [ ] **1.1 — [Step Title]**
  - **Context**: [What the executor needs to know]
  - **Action**: [Exactly what to do]
  - **Output**: [What gets created/modified]
  - **Verification**: [How to confirm it worked]
  - **Completion gate**: [When this item is done]
```

**Drift assessment:** PRD §25.4 specifies the 5-field schema **{Description, Context, Acceptance, Confidence, Verification}**. SKILL.md:1450-1460 currently uses **{Context, Action, Output, Verification, Completion gate}**. These overlap only on `Context` and `Verification`. A grep across SKILL.md for `Acceptance` and `TB-Add-8` returned zero hits (no `Acceptance` field exists in the current SKILL.md per-item structure). This is a **schema drift — the PRD-asserted §25.4 schema is not yet realized in SKILL.md** and will need to be landed as part of FR-CONV.1 (TB-Add catalogue) when TB-Add-8 enforcement is wired. See §7 Drift Notes below.

---

## 5. §25.5 Phase Contract: rf-qa → rf-qa-qualitative

**Source:** PRD `PRD_TASK_BUILDER_CONVERGENCE.md:989-1003`

### Verbatim YAML schema

```yaml
phase_contract:
  producer: rf-qa
  consumer: rf-qa-qualitative
  artifact: "## Inherited Structural Verdict block in spawn prompt"
  schema_version: "1.0.0"
  delivery_semantics: "at-most-once-per-cycle"
  freshness_rule: "On fix-cycle re-run, orchestrator re-injects NEW verdict; stale verdicts forbidden (INV-002)"
  enumeration_rule: "Checklist enumeration is dynamic — auto-picks up TB-Add catalogue from FR-CONV.1 (INV-010)"
  consumer_obligation: "Self-Audit listing relied-on PASS items AND ≥1 semantic check (INV-019)"
  anti_inflation: "Mechanical re-checking SKIPPED for PASS items; semantic verification STILL REQUIRED (rf-qa-qualitative.md:766-775)"
  failure_mode: "If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5"
```

### Per-field table (10 fields)

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `producer` | string | Yes | Upstream agent emitting artifact | **Fixed = `rf-qa`** (PRD:993) |
| `consumer` | string | Yes | Downstream agent consuming artifact | **Fixed = `rf-qa-qualitative`** (PRD:994) |
| `artifact` | string | Yes | What is exchanged | **Fixed = `"## Inherited Structural Verdict block in spawn prompt"`** (PRD:995). Cross-refs §25.2 |
| `schema_version` | string | Yes | Contract version | **Fixed = `"1.0.0"`** (PRD:996); semver |
| `delivery_semantics` | string | Yes | Delivery guarantee | **Fixed = `"at-most-once-per-cycle"`** (PRD:997) |
| `freshness_rule` | string | Yes | Reinjection-on-retry rule | On fix-cycle re-run, orchestrator re-injects NEW verdict; stale verdicts forbidden (**INV-002**) (PRD:998) |
| `enumeration_rule` | string | Yes | Checklist-enumeration dynamism | Checklist enumeration dynamic — auto-picks up TB-Add catalogue from FR-CONV.1 (**INV-010**) (PRD:999) |
| `consumer_obligation` | string | Yes | rf-qa-qualitative Self-Audit obligation | Self-Audit listing relied-on PASS items AND ≥1 semantic check (**INV-019**) (PRD:1000) |
| `anti_inflation` | string | Yes | Mechanical-recheck skip rule | Mechanical re-checking SKIPPED for PASS items; semantic verification STILL REQUIRED (**rf-qa-qualitative.md:766-775**) (PRD:1001) |
| `failure_mode` | string | Yes | Gate-halt on missing verdict | If rf-qa fails to emit verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5 (PRD:1002) |

---

## 6. Cross-Schema Consistency Check

| Claim | Verification | Status |
|-------|-------------|--------|
| §25.5 Phase Contract `artifact` references §25.2 Inherited Structural Verdict Block | §25.5 PRD:995 sets `artifact: "## Inherited Structural Verdict block in spawn prompt"`; §25.2 PRD:959 defines that exact header `"## Inherited Structural Verdict"`. Byte-match on the header string. | **CONSISTENT** |
| §25.5 `anti_inflation` cites rf-qa-qualitative.md:766-775 preserved by NFR-CONV.9 | §25.5 PRD:1001 cites `rf-qa-qualitative.md:766-775`. NFR-CONV.9 preserves that range (per task brief). The phase-contract field is the surface where the NFR is observed. | **CONSISTENT** |
| §25.3 `dedup_key` participates in FR-CONV.5 `F_n` cardinality per INV-012 | §25.3 PRD:974 defines `dedup_key = (assigned_files_range, escalation_ladder_exhaust_point)`. FR-CONV.5 uses `F_n` cardinality with INV-012 governing dedup collapse. `found_n_times` (PRD:975) is the counter that increments under dedup collapse — direct mechanical tie to `F_n`. | **CONSISTENT** |
| §25.4 `Context` field is enforced by TB-Add-8 (FR-CONV.1) | §25.4 PRD:983 inline comment: `# TB-Add-8 enforced`. FR-CONV.1 lands the TB-Add catalogue including TB-Add-8 = `file:line citation OR justified-absence`. | **CONSISTENT** |

All four cross-schema assertions hold. No internal contradictions detected between the 5 schemas.

---

## 7. Drift Notes

### Drift D-1: §25.4 Per-Item Schema not present in current SKILL.md

| Aspect | PRD §25.4 (target) | SKILL.md:1450-1460 (current) |
|--------|--------------------|------------------------------|
| Field set | `{Description, Context, Acceptance, Confidence, Verification}` | `{Context, Action, Output, Verification, Completion gate}` |
| Common fields | `Context`, `Verification` | `Context`, `Verification` |
| Missing from current | `Description`, `Acceptance`, `Confidence` | — |
| Extra in current | — | `Action`, `Output`, `Completion gate` |

**Evidence of absence:** `grep -n "Acceptance\|TB-Add-8" SKILL.md` returns zero hits (Bash output, this turn).

**Impact:** PRD §25.4 is asserted as `NFR-CONV.6 operational source — preserved unchanged by FRs`. However, the field set it preserves is **not the field set currently in SKILL.md:1450-1460**. Either (a) the "preserved unchanged" language refers to a different SKILL.md location that already contains the 5-field schema, or (b) FR-CONV.1 / TB-Add-8 must introduce this schema (so "preserved unchanged" semantics start with the FR-CONV landing). The task brief's framing (`per-item 5-field schema example for cross-reference`) suggests interpretation (a) was expected — but the line range cited (1450-1460) is the phase-template, not a per-item schema. This is a documentation pointer issue that should be reconciled in the TDD: either correct the line-range pointer or land the schema in SKILL.md.

### Drift D-2: §25.1 — degradation rule not encoded in schema YAML

§25.1's YAML schema shows the maximal form (`References`, `Source areas`, `Key constraints`). The degradation behavior ("when BUILD_REQUEST minimal, degrades to References-only") is asserted at the FR-CONV.2 level but not reflected as `Required: optional` markers in the schema body. This is a **specification ambiguity, not a schema contradiction** — but it means a consumer reading §25.1 in isolation would treat all three fields as required, while the FR-CONV.2 governing rule says two of them can be omitted under degradation. TDD should reconcile by either adding `# optional under degradation` comments to the schema or by writing the degradation rule into the schema metadata.

### No drift detected for §25.2, §25.3, §25.5

These three schemas have fixed-value fields whose strings are quoted verbatim in PRD §25. They are not currently emitted by SKILL.md (they are emitted by rf-qa / rf-qa-qualitative agent prompts at runtime), so there is no SKILL.md byte-match to perform. The PRD assertion stands as the canonical source.

---

## 8. Gaps and Questions

1. **§25.4 line-range pointer.** Task brief asserts `SKILL.md:1452-1457` contains the current per-item 5-field schema. Verification shows that range contains the *phase-template* (5 fields, but different field names). Question for TDD owner: is the per-item schema located elsewhere in SKILL.md, or is FR-CONV.1 responsible for landing it? (See Drift D-1.)
2. **Synthetic DNSP `evidence` stub format.** §25.3 PRD:972 allows `evidence` to be a stub citing log absence. The exact stub wording is not standardized — different agents may emit different stub strings, weakening dedup_key collision detection if `evidence` were ever folded into the dedup tuple. (It is not, per §25.3 PRD:974, so this is a soft concern only.)
3. **`dedup_key` storage type.** §25.3 PRD:974 declares the field as `tuple` in YAML, but YAML does not have a native tuple type — it would serialize as a list/sequence. Question: is the canonical wire format `[range, exhaust_point]` (list-of-2) or a single string `"(range, exhaust_point)"`? PRD:974 shows the string form. TDD should resolve to one canonical wire format.
4. **§25.5 `schema_version` evolution policy.** Fixed at `"1.0.0"` per PRD:996. No upgrade path documented (what triggers bump to 1.1.0 vs 2.0.0). Out of scope for this convergence release, but worth a backlog note.
5. **§25.5 `delivery_semantics: at-most-once-per-cycle`.** Implies idempotent consumption. Not stated whether rf-qa-qualitative is required to detect and reject a duplicate verdict within the same cycle. (`freshness_rule` covers cross-cycle re-injection; within-cycle duplicates not addressed.)

---

## 9. Stale Documentation Found

- **SKILL.md:1450-1460** does not contain the PRD §25.4 per-item 5-field schema. The task brief's expectation that this range contains the per-item schema (`Description/Context/Acceptance/Confidence/Verification`) does not match the file's current contents (`Context/Action/Output/Verification/Completion gate` phase template). See Drift D-1.
- No other staleness detected. §25.2, §25.3, §25.5 are agent-emitted runtime artifacts (not SKILL.md content), so no byte-match comparison applies.

---

## 10. Summary

The PRD §25 declares five mutually consistent schemas (Execution Context Header, Inherited Structural Verdict Block, Synthetic DNSP Finding, Per-Item Checklist Schema, Phase Contract). All four cross-schema consistency assertions hold: §25.5 `artifact` references §25.2 header verbatim; §25.5 `anti_inflation` preserves rf-qa-qualitative.md:766-775 per NFR-CONV.9; §25.3 `dedup_key` + `found_n_times` mechanize the INV-012 `F_n` cardinality; §25.4 `Context` is enforced by TB-Add-8. One material drift exists: the §25.4 Per-Item Schema (`Description/Context/Acceptance/Confidence/Verification`) is **not present** at SKILL.md:1450-1460 (which currently holds a `Context/Action/Output/Verification/Completion gate` phase template); FR-CONV.1 (TB-Add-8) must either land this schema or the PRD's "preserved unchanged" framing must be corrected to point to the actual current location. Two minor specification gaps remain (§25.1 degradation not encoded as optional markers; §25.3 `dedup_key` wire format ambiguous between tuple-string and YAML list).

**Status:** Complete
