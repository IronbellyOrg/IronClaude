# ISS-009: FR-3 severity rule tables are foundational but entirely new -- Proposals

## Issue Summary

FR-3 (Anchored Severity Rules) specifies that each structural checker has a severity rule table mapping `(dimension, mismatch_type) -> severity`. These tables are the foundation for all 5 structural checkers (FR-1), which feed into the deviation registry (FR-6), convergence gate (FR-7), and regression detection (FR-8). Zero rule table infrastructure exists in the codebase today. The only touchpoint is `compute_stable_id()` in convergence.py:28-31, which accepts `mismatch_type` as a hash input but has no rules to validate or assign severity from it.

## CRITICAL Dependency Check

Reviewed ISS-001 (convergence.py), ISS-002 (semantic_layer.py), and ISS-003 (remediate_executor.py) proposals in `spec-refactor/critical/`.

**No direct dependency on CRITICAL resolutions.** ISS-009 is about building new infrastructure (severity rule tables), not about reclassifying existing modules. The CRITICAL issues deal with CREATE-vs-MODIFY framing for existing modules; ISS-009 concerns genuinely new code that does not yet exist.

**Indirect connection**: ISS-001's proposed baseline section for FR-7 references `_check_regression()` which counts structural HIGHs -- those severities would originate from FR-3 rule tables. ISS-003's proposed delta list for FR-9 includes `RemediationPatch` which carries `finding_id` linking back to findings whose severity was assigned by rule tables. These are downstream consumers, not blockers. FR-3 rule tables can be built independently and should be built first.

## Codebase Ground Truth

**What exists:**
- `compute_stable_id(dimension, rule_id, spec_location, mismatch_type)` at `convergence.py:24-32` -- uses `mismatch_type` as a hash input but performs no severity lookup
- `Finding` dataclass at `models.py:22-56` -- has `severity: str`, `dimension: str`, `source_layer: str` fields but NO `rule_id`, `mismatch_type`, `stable_id`, `spec_quote`, or `roadmap_quote` fields
- `merge_findings()` at `convergence.py:96-152` -- fallback computes stable_id using `getattr(f, 'rule_id', '')` for BOTH `rule_id` and `mismatch_type` parameters (line 113), confirming the fields do not reliably exist on Finding yet
- Architecture design (architecture-design.md Section 3.3) defines `SeverityRule` frozen dataclass and `SeverityRuleTable = dict[str, SeverityLevel]` type alias -- but this is design doc only, not code
- Architecture design (Section 4.2.2) defines per-checker rule dicts with specific mismatch_type keys -- design doc only
- Tasklist phase-3 (T09) describes creating severity rule tables in `structural_checkers.py` or `severity_rules.py`

**What does NOT exist:**
- No `SeverityRule` or `SeverityRuleTable` type in any Python source file
- No `get_severity()` function anywhere
- No `SEVERITY_RULES` dict anywhere
- No `severity_rules.py` module
- No `structural_checkers.py` module
- Finding dataclass lacks `rule_id`, `mismatch_type`, `stable_id`, `spec_quote`, `roadmap_quote` fields (noted as ISS-024, LOW)

**Key observation**: The spec's FR-3 rule table (lines 143-160) and the architecture design's per-checker rule dicts (Section 4.2.2) use DIFFERENT mismatch_type keys for the same concepts:

| Concept | FR-3 Spec Key | Architecture Key |
|---------|---------------|-----------------|
| Roadmap references ID not in spec | (not explicitly named) | `phantom_id` |
| Function missing from roadmap | (not explicitly named) | `function_missing` |
| Parameter arity mismatch | (not explicitly named) | `param_arity` |
| Required spec file missing | (not explicitly named) | `file_missing` |
| Enum literal not covered | (not explicitly named) | `enum_uncovered` |

The spec uses prose descriptions in the "Mismatch Type" column, not machine-readable keys. The architecture design introduced machine keys but they do not appear in the spec itself. This gap must be resolved.

---

## Proposal A: Inline Rule Table with Canonical Keys -- Extend FR-3 In-Place

### Approach

Add canonical machine-readable mismatch_type keys directly to the FR-3 rule table in the spec. Add a `get_severity()` function signature and extensibility contract. Keep the rule table as a single flat dict keyed by `(dimension, mismatch_type)` tuples (matching the tasklist T09 pattern). Add a note that FR-3 has no v3.0 baseline -- it is genuinely new code.

### Before (Current Spec Text)

FR-3 section (lines 136-168):

```markdown
### FR-3: Anchored Severity Rules

**Description**: Each structural checker has a severity rule table that maps
specific structural mismatch types to fixed severity levels. Severity is NOT
LLM-judged for structural findings.

**Rule Examples**:

| Dimension | Mismatch Type | Severity |
|-----------|--------------|----------|
| Signatures | Roadmap references ID not in spec | HIGH |
| Signatures | Function missing from roadmap | HIGH |
| Signatures | Parameter arity mismatch | MEDIUM |
| Data Models | Required spec file missing from roadmap | HIGH |
| Data Models | File path prefix mismatch | HIGH |
| Data Models | Enum literal not covered | MEDIUM |
| Gates | Required frontmatter field not covered | HIGH |
| Gates | Step parameter missing | MEDIUM |
| Gates | Ordering constraint violated | MEDIUM |
| CLI | Config mode not covered | MEDIUM |
| CLI | Default value mismatch | MEDIUM |
| NFRs | Numeric threshold contradicted | HIGH |
| NFRs | Security primitive missing | HIGH |
| NFRs | Dependency direction violated | HIGH |
| NFRs | Coverage threshold mismatch | MEDIUM |

**Acceptance Criteria**:
- [ ] Every structural checker has an explicit rule table
- [ ] Rules are defined in code (not prompt text), keyed by `(dimension, mismatch_type) → severity`
- [ ] Same inputs always produce the same severity — no randomness, no LLM interpretation
- [ ] Rule table is extensible (new rules can be added without changing checker logic)

**Dependencies**: FR-1
```

### After (Proposed Spec Text)

```markdown
### FR-3: Anchored Severity Rules (New Module)

**Baseline**: No v3.0 code exists. This is genuinely new infrastructure.
`compute_stable_id()` in convergence.py accepts `mismatch_type` as a hash
input but performs no severity lookup. The `Finding` dataclass must be
extended with `rule_id` and `mismatch_type` fields (see ISS-024) before
rule tables can be consumed.

**Description**: A module-level severity rule table maps `(dimension,
mismatch_type)` tuples to fixed severity levels. Each structural checker
(FR-1) consumes this table to assign severity deterministically. Severity
is NOT LLM-judged for structural findings.

**Canonical Rule Table**:

| Dimension | Mismatch Type (key) | Human Description | Severity |
|-----------|-------------------|-------------------|----------|
| signatures | `phantom_id` | Roadmap references ID not in spec | HIGH |
| signatures | `function_missing` | Spec function absent from roadmap | HIGH |
| signatures | `param_arity` | Parameter count mismatch | MEDIUM |
| signatures | `id_missing` | Spec ID not referenced in roadmap | MEDIUM |
| data_models | `file_missing` | Required spec file missing from roadmap | HIGH |
| data_models | `path_prefix` | File path prefix mismatch | HIGH |
| data_models | `enum_uncovered` | Enum literal not covered | MEDIUM |
| data_models | `field_missing` | Dataclass field not referenced | MEDIUM |
| gates | `frontmatter_field` | Required frontmatter field not covered | HIGH |
| gates | `step_param` | Step parameter missing | MEDIUM |
| gates | `ordering` | Ordering constraint violated | MEDIUM |
| cli | `mode_uncovered` | Config mode not covered | MEDIUM |
| cli | `default_mismatch` | Default value mismatch | MEDIUM |
| nfrs | `threshold_contradicted` | Numeric threshold contradicted | HIGH |
| nfrs | `security_missing` | Security primitive missing | HIGH |
| nfrs | `dependency_violated` | Dependency direction violated | HIGH |
| nfrs | `coverage_mismatch` | Coverage threshold mismatch | MEDIUM |

**Implementation contract**:
- Data structure: `SEVERITY_RULES: dict[tuple[str, str], str]` keyed by
  `(dimension, mismatch_type)` tuple.
- Lookup function: `get_severity(dimension: str, mismatch_type: str) -> str`
  returning the severity level. Raises `KeyError` for unknown mismatch types
  (fail-fast, not fail-silent).
- Location: Co-located with structural checkers in `structural_checkers.py`
  or a dedicated `severity_rules.py` module.

**Semantic boundary**: Structural checkers declare their `mismatch_type` keys
via these rule tables. Any aspect of spec-vs-roadmap comparison NOT covered
by any checker's declared mismatch types belongs to the semantic layer (FR-4).

**Acceptance Criteria**:
- [ ] Every structural checker has an explicit rule table
- [ ] Rules are defined in code (not prompt text), keyed by `(dimension, mismatch_type) -> severity`
- [ ] Same inputs always produce the same severity -- no randomness, no LLM interpretation
- [ ] Rule table is extensible (new rules can be added without changing checker logic)
- [ ] `get_severity()` lookup function exists and raises `KeyError` for unknown types
- [ ] Mismatch type keys match the canonical keys in this table (not prose descriptions)
- [ ] Finding dataclass carries `rule_id` and `mismatch_type` fields populated by checkers

**Dependencies**: FR-1 (consumer), ISS-024 (Finding field extension)
```

### Trade-offs

**Pros:**
- Self-contained: spec now has canonical machine keys, not just prose descriptions
- Aligns spec with architecture design's per-checker rule dicts
- Adds the "genuinely new" baseline statement consistent with CRITICAL proposals' pattern
- Adds concrete implementation contract (data structure, lookup function, location)
- Surfaces the ISS-024 dependency (Finding fields) that is currently buried in LOW issues
- Adds 4 mismatch types from architecture design not in original spec (`id_missing`, `field_missing` for signatures/data_models)

**Cons:**
- Larger edit surface than the other proposals
- Introducing canonical keys in the spec creates a naming contract that constrains implementation
- The `KeyError` behavior for unknown types is a design choice that could be debated (vs returning a default)

---

## Proposal B: Phased Validation Approach -- Split FR-3 into FR-3a (Schema) and FR-3b (Calibration)

### Approach

Acknowledge that severity rule tables are both a schema problem (defining the structure) and a calibration problem (choosing correct severity levels). Split FR-3 into two sub-requirements: FR-3a defines the rule table infrastructure and data structure; FR-3b defines the specific severity assignments and mandates validation against real findings from v3.0 runs. This addresses the compatibility report's concern (Section 7e) that "if the rule tables are wrong, all 5 checkers produce incorrect findings."

### Before (Current Spec Text)

Same as Proposal A -- FR-3 section, lines 136-168.

### After (Proposed Spec Text)

```markdown
### FR-3a: Severity Rule Table Infrastructure (New Module)

**Baseline**: No v3.0 code exists. Genuinely new infrastructure.

**Description**: Define the severity rule table schema and lookup mechanism.
Each structural checker (FR-1) will consume this table to assign severity
deterministically. The table maps `(dimension, mismatch_type)` tuples to
fixed severity levels (HIGH, MEDIUM, LOW).

**Implementation contract**:
- Type: `SeverityRuleTable = dict[str, SeverityLevel]` per checker
  (keyed by mismatch_type, dimension implicit from checker)
- Global lookup: `get_severity(dimension: str, mismatch_type: str) -> str`
- Each checker declares its own `rules: SeverityRuleTable` attribute
- Unknown mismatch types raise `KeyError` (fail-fast)
- Location: `structural_checkers.py` (co-located with checkers)

**Acceptance Criteria** (FR-3a):
- [ ] `SeverityRuleTable` type alias defined
- [ ] `get_severity()` lookup function exists and is deterministic
- [ ] Each checker class has a `rules` attribute of type `SeverityRuleTable`
- [ ] Extensible: adding a rule requires only a dict entry, not checker logic changes
- [ ] Unknown mismatch_type raises `KeyError`, not silent default

### FR-3b: Severity Calibration and Validation

**Description**: Populate the rule tables with specific severity assignments
and validate them against real-world findings. The initial calibration uses
findings from v3.0 runs (Appendix B) as ground truth. Severity assignments
must be validated before structural checkers are trusted for gate decisions.

**Canonical Severity Assignments**:

| Dimension | Mismatch Type | Severity | Validation Source |
|-----------|--------------|----------|-------------------|
| signatures | `phantom_id` | HIGH | Appendix B: Phantom FR-009..FR-038 IDs |
| signatures | `function_missing` | HIGH | Appendix B: `gate_passed()` signature |
| signatures | `param_arity` | MEDIUM | Appendix B: `ast_analyze_file()` dual placement |
| data_models | `file_missing` | HIGH | Appendix B: Missing `wiring_config.py` |
| data_models | `path_prefix` | HIGH | Appendix B: `audit/` vs `cli/audit/` |
| data_models | `enum_uncovered` | MEDIUM | (no v3.0 example) |
| gates | `frontmatter_field` | HIGH | Appendix B: `audit_artifacts_used` omission |
| gates | `step_param` | MEDIUM | Appendix B: Missing step parameters |
| gates | `ordering` | MEDIUM | Appendix B: Stricter phasing than spec |
| cli | `mode_uncovered` | MEDIUM | (no v3.0 example) |
| cli | `default_mismatch` | MEDIUM | (no v3.0 example) |
| nfrs | `threshold_contradicted` | HIGH | Appendix B: `<2s` vs `<5s` |
| nfrs | `security_missing` | HIGH | Appendix B: Missing `yaml.safe_dump()` |
| nfrs | `dependency_violated` | HIGH | (no v3.0 example) |
| nfrs | `coverage_mismatch` | MEDIUM | (no v3.0 example) |

**Acceptance Criteria** (FR-3b):
- [ ] All 15+ mismatch types from the canonical table are populated
- [ ] At least 9 rules validated against real v3.0 findings (Appendix B)
- [ ] Rules without v3.0 validation examples are flagged for manual review
- [ ] Same inputs always produce same severity (determinism test)

**Dependencies**: FR-3a (infrastructure), FR-1 (consumer)
```

### Trade-offs

**Pros:**
- Separates infrastructure (unambiguous, build-once) from calibration (requires judgment, may need tuning)
- Links severity assignments to real evidence (Appendix B), addressing the "if the rule tables are wrong" risk
- Makes explicit that 6 of 15 rules have no v3.0 validation evidence and need manual review
- Enables parallel work: FR-3a can be built while FR-3b calibration is debated

**Cons:**
- Splitting FR-3 into sub-requirements increases spec complexity and may break references
- Any document citing "FR-3" must now specify FR-3a or FR-3b
- The FR-7/FR-8 dependency chain references "FR-3" generically; splitting may require updating FR-1's dependency line
- Validation against Appendix B is useful but not a gate -- real deviations may not match v3.0 patterns exactly

---

## Proposal C: Minimal Patch -- Add Baseline Statement and Key Mapping Only

### Approach

Make the smallest possible change to FR-3: add a baseline statement confirming no code exists, add canonical mismatch_type keys as a column in the existing table, and note the Finding field dependency. Do not restructure FR-3, do not add implementation contract details, do not split into sub-requirements. Relies on the architecture design document and tasklist T09 for implementation details.

### Before (Current Spec Text)

Same as Proposal A -- FR-3 section, lines 136-168.

### After (Proposed Spec Text)

```markdown
### FR-3: Anchored Severity Rules

**Baseline**: No v3.0 code exists. Genuinely new infrastructure.
`compute_stable_id()` accepts `mismatch_type` as input but no severity
lookup or rule table code exists. Finding dataclass requires `rule_id`
and `mismatch_type` field additions (ISS-024).

**Description**: Each structural checker has a severity rule table that maps
specific structural mismatch types to fixed severity levels. Severity is NOT
LLM-judged for structural findings.

**Rule Table** (canonical keys):

| Dimension | Mismatch Key | Description | Severity |
|-----------|-------------|-------------|----------|
| signatures | `phantom_id` | Roadmap references ID not in spec | HIGH |
| signatures | `function_missing` | Function missing from roadmap | HIGH |
| signatures | `param_arity` | Parameter arity mismatch | MEDIUM |
| data_models | `file_missing` | Required spec file missing from roadmap | HIGH |
| data_models | `path_prefix` | File path prefix mismatch | HIGH |
| data_models | `enum_uncovered` | Enum literal not covered | MEDIUM |
| gates | `frontmatter_field` | Required frontmatter field not covered | HIGH |
| gates | `step_param` | Step parameter missing | MEDIUM |
| gates | `ordering` | Ordering constraint violated | MEDIUM |
| cli | `mode_uncovered` | Config mode not covered | MEDIUM |
| cli | `default_mismatch` | Default value mismatch | MEDIUM |
| nfrs | `threshold_contradicted` | Numeric threshold contradicted | HIGH |
| nfrs | `security_missing` | Security primitive missing | HIGH |
| nfrs | `dependency_violated` | Dependency direction violated | HIGH |
| nfrs | `coverage_mismatch` | Coverage threshold mismatch | MEDIUM |

**Acceptance Criteria**:
- [ ] Every structural checker has an explicit rule table
- [ ] Rules are defined in code (not prompt text), keyed by `(dimension, mismatch_type) -> severity`
- [ ] Same inputs always produce the same severity -- no randomness, no LLM interpretation
- [ ] Rule table is extensible (new rules can be added without changing checker logic)

**Dependencies**: FR-1, ISS-024 (Finding field extension)
```

### Trade-offs

**Pros:**
- Minimal disruption -- preserves FR-3 structure, acceptance criteria, and dependencies
- Adds baseline statement consistent with CRITICAL proposals' pattern
- Adds canonical keys that bridge the gap between prose descriptions and code
- Does not constrain implementation beyond what the architecture design already specifies
- Easy to review: changes are a baseline paragraph, one column addition to the table, and one dependency addition

**Cons:**
- Does not add implementation contract (data structure, lookup function, location) -- defers to architecture design and tasklist
- Does not address the calibration/validation concern raised in Section 7e
- Missing 4 mismatch types that the architecture design added (`id_missing`, `field_missing` for signatures/data_models)
- Does not surface the semantic boundary definition (which is currently in FR-4's description, not FR-3)

---

## Recommended Proposal

**Proposal A (Inline Rule Table with Canonical Keys)** is recommended.

**Rationale:**

1. **Completeness without over-engineering**: Proposal A adds canonical keys, implementation contract, baseline statement, semantic boundary reference, and surfaces the ISS-024 dependency -- all within the existing FR-3 structure. It does not split FR-3 (avoiding the reference-breakage risk of Proposal B) and does not defer critical details to external documents (avoiding the incompleteness of Proposal C).

2. **Consistency with CRITICAL proposals**: The ISS-001 and ISS-003 proposals both use the "Baseline + Description + Implementation detail" pattern. Proposal A follows this same pattern for FR-3, creating a consistent spec structure.

3. **Foundation risk mitigation**: Section 7e flags FR-3 as a cascading dependency. Proposal A makes the spec maximally precise about what must be built, reducing the risk of misimplementation. The 4 additional mismatch types from the architecture design (that the original spec omitted) are included, preventing a gap between spec and design doc.

4. **No CRITICAL dependency blocker**: FR-3 is genuinely new code with no v3.0 baseline conflict. It can be implemented immediately. The only prerequisite is ISS-024 (Finding field extension), which is a LOW-severity additive change.

**If ISS-024 will be resolved as part of the same refactoring pass**, Proposal A is fully self-contained. If ISS-024 is deferred, add a note that FR-3 implementation must stub the Finding fields until ISS-024 lands.

**Proposal B is the fallback** if the team wants to validate severity calibration against real v3.0 findings before trusting the rule tables for gate decisions. This is a sound engineering concern but adds spec complexity that may not be justified given that the severity assignments were already adversarial-reviewed (BF-3, BF-6).
