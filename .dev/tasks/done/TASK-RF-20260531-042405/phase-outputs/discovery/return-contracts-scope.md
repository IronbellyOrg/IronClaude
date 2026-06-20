# R1.1 RETURN_CONTRACTS + Threshold Registry Scope

**Phase:** 6 (R1.1 — extend `superclaude.contracts` with `RETURN_CONTRACTS` + full threshold registry)
**Source-authority refs:** BUILD-REQUEST §R1.1 + §MVR §5 + §Contract items #5/#8; master:§Recurrence #7 + §Flaw 5; `phase-outputs/discovery/contracts-consumer-sites.md` §C+§D+§F (R0.3 inventory); `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:425-460` (canonical return-contract prose).
**Generated:** Phase 6 Step 6.1 (2026-06-01).
**Worktree:** `refactor/roadmap-pipeline-r0-r1-rewrite` at `/config/workspace/IronClaude-RoadmapRewrite/`, parent commit `1c56b50f`.

---

## A. R0.3 baseline (recap — unchanged in R1.1)

`src/superclaude/contracts/__init__.py` already exports (per R0.3 commit `bdfad6d3`):

- `ID_PATTERNS: dict[str, str]` — 5 keys (`FR`, `NFR`, `SC`, `G`, `D`)
- `CONVERGENCE_THRESHOLDS: dict[str, tuple[float, float]]` — 2 keys (`sc:roadmap`, `sc:release-split`)
- `GATE_FIELD_NAMES: dict[str, dict[str, str]]` — 1 nested entry (`deviation_analysis.ambiguous`)

R1.1 **extends** this surface — the three R0.3 constants are not modified, only added to `__all__`.

---

## B. Skill-prose grep — only `sc:adversarial` declares a programmatic return contract

Grep over `src/superclaude/skills/` for `return_contract` / `RETURN:` / `OUTPUT:` / `output_schema`:

| Skill file | Line | Construct | Programmatic return? |
|---|---|---|---|
| `sc-adversarial-protocol/SKILL.md` | 432-443 | `return_contract:` YAML block w/ 10 typed fields | **YES** (canonical) |
| `sc-adversarial-protocol/SKILL.md` | 2085-2107 | `return_contract:` field-table reiteration (T05.07) | YES (same shape as L432) |
| `sc-adversarial-protocol/SKILL.md` | 2787-2792 | `return_contract:` inside pipeline-manifest phase schema | YES (subset of L432) |
| `sc-adversarial-protocol/SKILL.md` | 2470-2474 | `output_schema:` for DAG output | NO (internal DAG, not skill return) |
| `sc-roadmap-protocol/refs/adversarial-integration.md` | 370, 384 | `return_contract:` references | NO (references the sc:adversarial contract from B above) |
| `sc-validate-roadmap-protocol/SKILL.md` | 451 | `OUTPUT: Write report to {OUTPUT_DIR}/01-agent-D{N}-{domain-slug}.md` | NO (file-output instruction, not return) |
| `sc-crash-recovery/refs/investigators.md` | 118 | `Return:` (investigator-internal) | NO (sub-agent return, not skill-level) |
| `sc-review-translation-protocol/SKILL.md` | 76 | `Output: Context Summary for User Confirmation` | NO (user output, not programmatic return) |

**Conclusion:** Only **one skill** (`sc:adversarial`) declares a programmatic, parseable return contract per BUILD-REQUEST §MVR §5. The canonical example `RETURN_CONTRACTS = {"sc:adversarial": AdversarialReturn}` is the complete R1.1 surface — no fabrication of additional skill contracts.

---

## C. Canonical `AdversarialReturn` shape (verbatim from `sc-adversarial-protocol/SKILL.md:432-443`)

```yaml
return_contract:
  merged_output_path: "<path to merged file>"       # null if merge not reached
  convergence_score: 0.75                            # float 0.0-1.0, null if debate not reached
  artifacts_dir: "<path to adversarial/ directory>"  # always set (created at pipeline start)
  status: "success"                                  # success | partial | failed
  base_variant: "opus:architect"                     # model:persona that won debate, null if not reached
  unresolved_conflicts: 2                            # integer count of unresolved diff points, 0 on success
  fallback_mode: false                               # true if pipeline used fallback path
  failure_stage: null                                # null on success; "variant_generation" | "debate" | "merge" | "validation" | "transport"
  invocation_method: "skill-direct"                  # "skill-direct" | "task-agent" | "manual"
  unaddressed_invariants: []                         # list of HIGH-severity UNADDRESSED items from invariant probe
```

**Field table** (verbatim from SKILL.md:449-460):

| Field | Type | Notes |
|---|---|---|
| `merged_output_path` | `str \| None` | Path; None if merge not reached |
| `convergence_score` | `float \| None` | 0.0-1.0; None if debate not reached |
| `artifacts_dir` | `str` | Always set |
| `status` | enum: `success` \| `partial` \| `failed` | |
| `base_variant` | `str \| None` | `model:persona`; None if debate not reached |
| `unresolved_conflicts` | `int` | 0 on success |
| `fallback_mode` | `bool` | True if any fallback used |
| `failure_stage` | `str \| None` | `variant_generation` \| `debate` \| `merge` \| `validation` \| `transport` |
| `invocation_method` | enum: `skill-direct` \| `task-agent` \| `manual` | |
| `unaddressed_invariants` | `tuple[UnaddressedInvariant, ...]` | Each item: `{id, category, assumption, severity}` per SKILL.md:460 |

**Hashability constraint** (Step 6.2 instruction: "dataclasses are frozen and hashable"): `unaddressed_invariants` must be `tuple[UnaddressedInvariant, ...]` (immutable + hashable) — not `list[dict]`. A nested frozen `UnaddressedInvariant` dataclass keeps the parent hashable.

---

## D. Consumer modules (sites that parse `AdversarialReturn` shape)

Grep over `src/superclaude/cli/` for the canonical fields (`convergence_score`, `base_variant`, `artifacts_dir`, `merged_output_path`):

| File | Line | Construct | Role |
|---|---|---|---|
| `src/superclaude/cli/roadmap/prompts.py` | 896 | LLM-prompt text: `"- convergence_score: (float 0.0-1.0 ...)"` | Tells LLM what frontmatter field to emit |
| `src/superclaude/cli/roadmap/prompts.py` | 922 | LLM-prompt text: `"- base_variant: (string: the identifier ...)"` | Same as above |
| `src/superclaude/cli/roadmap/gates.py` | 380-388 | `_convergence_score_valid` parses `convergence_score` from frontmatter | Gate predicate |
| `src/superclaude/cli/roadmap/gates.py` | 1253-1266 | Frontmatter required fields: `convergence_score`, `rounds_completed`, `base_variant`, `variant_scores` | Adversarial gate spec |
| `src/superclaude/cli/roadmap/executor.py` | 2042 | `debate_file = out / "debate-transcript.md"` | Artifact path (not field read) |

**Integration boundary:** sc:adversarial writes a markdown artifact with frontmatter; roadmap CLI parses that frontmatter. The 10-field `return_contract` becomes the canonical frontmatter schema. R1.1 makes the field names + types discoverable via `RETURN_CONTRACTS["sc:adversarial"]` so consumers can validate without re-asserting the shape inline.

R1.1 does **not** rewrite the prompts.py prose or gates.py predicates in this phase — those would change consumer behavior. R1.1 only introduces the SoT dataclass; PG6.1 verifies no consumer over-couples.

---

## E. Extended threshold registry — scalars in scope for R1.1

Per `contracts-consumer-sites.md §C` plus a new finding (§F below). Behavioral float thresholds currently inlined as default args or in-function literals:

| File | Line | Literal | Semantic name | R1.1 migration target |
|---|---|---|---|---|
| `src/superclaude/cli/roadmap/fingerprint.py` | 171 | `min_coverage_ratio: float = 0.7` (default arg, `check_fingerprint_coverage`) | `fingerprint.coverage_min` | YES (behavioral) |
| `src/superclaude/cli/roadmap/fingerprint.py` | 205 | `min_coverage_ratio: float = 0.7` (default arg, `fingerprint_gate_passed`) | `fingerprint.coverage_min` | YES (behavioral) |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | 91 | `threshold: float = 0.5` (default arg, `check_extraction_adequacy`) | `structural_audit.adequacy_min` | YES (behavioral) |
| `src/superclaude/cli/roadmap/gates.py` | 375 | `return float(value) >= 0.7` (gate predicate body — NEW finding, see §F) | `fingerprint.coverage_min` | YES (behavioral) |
| `src/superclaude/cli/roadmap/gates.py` | 363, 365, 1481 | docstring + failure_message prose containing `"0.7"` | n/a (display string) | Optional (f-string render); leave-as-is acceptable per Phase 4 §F note |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | 101 | docstring prose `"(0.5)"` | n/a | Optional; leave-as-is |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | 43-46 | `_FR_HEADING_RE` composes `r"^#{1,6}\s+.*?\b(FR-\d+(?:\.\d+)?)\b"` | n/a (regex composition, not a threshold) | YES (composition migration — see §G) |

**Proposed `THRESHOLDS` shape:**

```python
THRESHOLDS: Final[dict[str, float]] = {
    "fingerprint.coverage_min": 0.7,
    "structural_audit.adequacy_min": 0.5,
}
```

Hierarchical dotted keys (`module.metric`) keep the registry future-extensible without nested dicts.

---

## F. Phase 4 inventory deltas (informational deviations)

Phase 4 Step 4.1 `contracts-consumer-sites.md §C/§D/§F` enumerated R1.1-scope rows but missed one **behavioral** site:

**D3 (Phase 6 finding):** `src/superclaude/cli/roadmap/gates.py:375` contains `return float(value) >= 0.7` — a live behavioral threshold inside `_fingerprint_coverage_check`. Phase 4 catalogued only the surrounding prose (L363, L365, L1481 docstring/failure_message). This is a true behavioral migration target for Step 6.3, not just prose rendering.

**Logged here** rather than back-edited into the closed Phase 4 doc per Contract #1 immutability of merged phase artifacts. The R0 acceptance report (`r0-acceptance-report.md`) is unaffected because the gate predicate was never claimed cleaned in R0.

---

## G. `_FR_HEADING_RE` composition (fidelity_checker.py:43-46)

Current literal:

```python
_FR_HEADING_RE = re.compile(
    r"^#{1,6}\s+.*?\b(FR-\d+(?:\.\d+)?)\b",
    re.MULTILINE,
)
```

The pattern composes three parts:
1. Heading prefix: `^#{1,6}\s+.*?\b` (heading-anchored, structural)
2. Canonical FR body: `FR-\d+(?:\.\d+)?` (= `ID_PATTERNS["FR"]`)
3. Word-boundary suffix: `\b`

R1.1 migration (preserves capture group + behavior):

```python
from superclaude.contracts import ID_PATTERNS

_FR_HEADING_RE = re.compile(
    rf"^#{{1,6}}\s+.*?\b({ID_PATTERNS['FR']})\b",
    re.MULTILINE,
)
```

The `\b…\b` word boundaries stay local (rendering concern); the pattern body lives in SoT. The doubled `{{` / `}}` escape the f-string brace literals for the regex quantifier.

---

## H. Arch-lint extension scope (Step 6.3)

The existing walker (`src/superclaude/tools/arch_lint.py`, R0.3 commit `bdfad6d3`) auto-discovers canonical names from `superclaude.contracts.__all__`. Once Step 6.2 adds `AdversarialReturn`, `RETURN_CONTRACTS`, `UnaddressedInvariant`, `THRESHOLDS` to `__all__`, the existing **name-rebind** rule (Assign/AnnAssign targeting a canonical name) automatically extends to those constants.

**New rule added in Step 6.3 (ClassDef detection):**

The existing walker checks `ast.Assign` and `ast.AnnAssign` but not `ast.ClassDef`. A consumer could write `class AdversarialReturn: ...` outside the contracts module and evade detection. Step 6.3 adds a third rule:

```python
# Rule 3: class definition shadowing a canonical name.
if isinstance(node, ast.ClassDef) and node.name in canonical_names:
    if _line_has_allow_marker(source_lines, node.lineno):
        continue
    violations.append(
        Violation(
            path=path,
            lineno=node.lineno,
            kind="class-redef",
            name=node.name,
            detail=(
                "dataclass owned by superclaude.contracts; "
                "import instead of redefine"
            ),
        )
    )
```

**Float-literal detection (deliberately out of scope):** Extending literal-duplicate from string-bodies to float values (e.g., flagging every `0.7` outside contracts) would be impractical — `0.7`/`0.5` legitimately appear in unrelated code (tests, math, configs). The name-rebind rule on `THRESHOLDS` is sufficient; `tests/roadmap/test_threshold_registry.py` parametrized tests cover the orphan-literal sweep at integration level.

---

## I. Migration plan (Step 6.3)

R1.1-scope migrations (perform in Step 6.3):

1. **`fingerprint.py:171, 205`** — replace `min_coverage_ratio: float = 0.7` default with `from superclaude.contracts import THRESHOLDS` + `min_coverage_ratio: float = THRESHOLDS["fingerprint.coverage_min"]`. (Note: function-default-arg form `def f(x: float = THRESHOLDS["fingerprint.coverage_min"]):` works because dict-key access is evaluated at module load — same as a module-level constant.)
2. **`spec_structural_audit.py:91`** — same pattern with `THRESHOLDS["structural_audit.adequacy_min"]`.
3. **`gates.py:375`** — replace `>= 0.7` literal with `>= THRESHOLDS["fingerprint.coverage_min"]`; add `from superclaude.contracts import THRESHOLDS` to gates.py imports if not already present.
4. **`fidelity_checker.py:43-46`** — replace inline FR pattern with f-string composition (§G above); add `from superclaude.contracts import ID_PATTERNS`.

R1.1-scope deferrals (do NOT migrate in Step 6.3):

- `gates.py:363, 365, 1481` docstring/failure_message prose containing `"0.7"` — leave as-is (display string, not behavioral; `# arch-lint: allow-duplicate prose-render` not needed because arch-lint does not flag float literals).
- `spec_structural_audit.py:101` docstring `"(0.5)"` — leave as-is.
- `executor.py:1808` prose comment — left out per Phase 4 §D classification (prose-only, no behavior).
- `integration_contracts.py` — left out per Phase 4 §F (no in-file literals).

R1.1 consumer migrations (return-contract side):

- `prompts.py:896, 922` LLM-prompt text — NOT migrated. Rationale: the prompt prose teaches the LLM the frontmatter schema; coupling it to `RETURN_CONTRACTS` would over-couple the LLM-side text generation to the consumer-side typing. The SoT dataclass is for consumer validation, not prompt assembly. Phase 11 (R1.6 cleanup) may revisit if Step 6.4 / PG6.1 surface a coupling argument.
- `gates.py:380-388, 1253-1266` frontmatter parsing — NOT migrated. Rationale: gates parse YAML frontmatter, not a Python `AdversarialReturn` instance. A future R1.2 envelope migration (Phase 7) may introduce a typed bridge; until then the SoT shape is informational + arch-lint enforced.

**Net R1.1 behavioral migration: 4 sites (fingerprint x2, spec_structural_audit, gates.py:375, fidelity_checker).**

---

## J. Tests scope (Step 6.4)

Extend `tests/roadmap/test_threshold_registry.py` with parametrized cases:

- `test_constant_defined_exactly_once_in_src` — extend `parametrize` to include `RETURN_CONTRACTS`, `THRESHOLDS`, `AdversarialReturn`, `UnaddressedInvariant`.
- `test_r1_1_consumers_import_from_contracts` — NEW parametrized over R1.1 consumer files: fingerprint.py, spec_structural_audit.py, gates.py, fidelity_checker.py.
- `test_return_contracts_shape_matches_skill_prose` — NEW. Reads `sc-adversarial-protocol/SKILL.md` field table, asserts `AdversarialReturn` field names match (sentinel against drift).
- `test_thresholds_shape_matches_consumer_sites` — NEW. Asserts `THRESHOLDS["fingerprint.coverage_min"] == 0.7` and `THRESHOLDS["structural_audit.adequacy_min"] == 0.5` verbatim per Phase 4 inventory.
- `test_adversarial_return_is_frozen_hashable` — NEW unit test (in `tests/contracts/`). Constructs an instance, asserts `hash()` works.

Extend `tests/contracts/test_arch_lint.py` with:

- `test_class_redef_violation_detected` — NEW. Synthetic `class AdversarialReturn: ...` file → walker emits `class-redef` violation.
- `test_canonical_names_includes_r1_1_extensions` — NEW. Imports `superclaude.contracts.__all__`, asserts membership of `AdversarialReturn`, `RETURN_CONTRACTS`, `THRESHOLDS`, `UnaddressedInvariant`.

---

**Discovery complete.** R1.1 migration set: 4 behavioral files (fingerprint, spec_structural_audit, gates, fidelity_checker). Skill contracts: 1 (sc:adversarial → AdversarialReturn). Arch-lint extension: 1 new rule (ClassDef redef). Tests: 5 new parametrized/unit cases. New finding logged: Phase 6 D3 (gates.py:375 behavioral 0.7 missed in Phase 4 inventory).
