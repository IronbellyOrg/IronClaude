# R0.3 Contracts Consumer Inventory

**Phase:** 4 (R0.3 — `superclaude.contracts` SoT module + arch-lint)
**Source-authority refs:** BUILD-REQUEST §R0 item 3 + §MVR §5 + §Contract items #5/#8; master:§Recurrence #7 + master:§Flaw 5; research/01-file-inventory.md §E (confirms `superclaude.contracts` does NOT exist today) + §F (touch matrix).
**Generated:** Phase 4 Step 4.1 (2026-06-01).

## A. Pre-existence check

`superclaude.contracts` directory absent in `src/superclaude/` (verified via `ls`). Pyproject `[tool.hatch.build.targets.wheel] packages = ["src/superclaude"]` is recursive-by-prefix — Hatchling auto-discovers any new subpackage under `src/superclaude/`, so no explicit pyproject edit is required for the new module.

## B. Consumer sites — verbatim ID-pattern literals

| File | Line | Literal type | Current literal value | Will migrate in phase |
|---|---|---|---|---|
| `src/superclaude/cli/roadmap/spec_parser.py` | 325 | ID_PATTERN.FR | `re.compile(r"\bFR-\d+(?:\.\d+)?\b")` | **R0.3** (canonicalize as `ID_PATTERNS["FR"] = r"FR-\d+(?:\.\d+)?"`) |
| `src/superclaude/cli/roadmap/spec_parser.py` | 326 | ID_PATTERN.NFR | `re.compile(r"\bNFR-\d+(?:\.\d+)?\b")` | **R0.3** (canonicalize as `ID_PATTERNS["NFR"] = r"NFR-\d+"` per BUILD-REQUEST §MVR §5; note: in-file pattern is broader — see §D below for the resolved approach) |
| `src/superclaude/cli/roadmap/spec_parser.py` | 327 | ID_PATTERN.SC | `re.compile(r"\bSC-\d+\b")` | **R0.3** |
| `src/superclaude/cli/roadmap/spec_parser.py` | 328 | ID_PATTERN.G | `re.compile(r"\bG-\d+\b")` | **R0.3** (G family added in Phase 2 D1 informational deviation — must be in SoT per Contract #8) |
| `src/superclaude/cli/roadmap/spec_parser.py` | 329 | ID_PATTERN.D | `re.compile(r"\bD-?\d+\b")` | **R0.3** |
| `src/superclaude/cli/roadmap/id_registry.py` | 37 | ID_PATTERN_KEYS tuple | `_ID_PATTERN_KEYS: tuple[str, ...] = ("FR", "NFR", "SC", "G", "D")` | **R0.3** (replace with `tuple(ID_PATTERNS.keys())`) |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | 43-46 | ID_PATTERN.FR (heading variant) | `r"^#{1,6}\s+.*?\b(FR-\d+(?:\.\d+)?)\b"` | **R1.1** (heading-anchored regex composes a structural prefix `^#{1,6}\s+.*?` + the base FR pattern; composition logic deferred to R1.1's broader threshold/regex registry — see §D) |

**ID-pattern occurrences outside `src/superclaude/cli/roadmap/`:** none found via `grep -rnE '(FR-\\d|NFR-\\d|SC-\\d|G-\\d|D-?\\d)' src/superclaude/cli/roadmap/`. Tests reference IDs but as literal strings (e.g. `"FR-1"`), not regex literals — out of arch-lint scope.

## C. Consumer sites — verbatim convergence-threshold literals

| File | Line | Literal type | Current literal value | Will migrate in phase |
|---|---|---|---|---|
| `src/superclaude/cli/roadmap/fingerprint.py` | 171, 205 | CONVERGENCE_THRESHOLD (fingerprint min_coverage_ratio) | `min_coverage_ratio: float = 0.7` | **R1.1** — this is the *fingerprint coverage ratio*, an adjacent (not identical) concept to the `(0.7, 0.5)` convergence pair in `CONVERGENCE_THRESHOLDS["sc:roadmap"]` per BUILD-REQUEST §MVR §5. R1.1 extends `superclaude.contracts` with the full threshold registry and reconciles. |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | 91, 101, 103 | structural-audit threshold (default arg + prose) | `threshold: float = 0.5` | **R1.1** — adjacent, similar to fingerprint above. Defer to R1.1. |
| `src/superclaude/cli/roadmap/gates.py` | 356-358, 1474 | anti-instinct/fingerprint gate threshold (prose constant) | `fingerprint_coverage must be >= 0.7` in docstring + `failure_message="fingerprint_coverage must be >= 0.7; ..."` | **R1.1** — prose-only; R1.1's registry will allow rendering the value rather than hardcoding the literal string. |
| `src/superclaude/cli/roadmap/convergence.py` | (none) | `(0.7, 0.5)` pair | **not present as literal pair** — convergence module uses its own cost-budget constants (L25-31), not the SoT convergence pair | n/a — SoT pair is introduced by R0.3 as a forward-looking SoT entry per BUILD-REQUEST §MVR §5 example. No existing literal to migrate. |
| `src/superclaude/cli/roadmap/commands.py` | (none) | `(0.7, 0.5)` pair | not present | n/a (PRESERVE per MVR §6.3) |

**Resolution:** R0.3 lands the `CONVERGENCE_THRESHOLDS = {"sc:roadmap": (0.7, 0.5), "sc:release-split": (0.7, 0.5)}` dict as a forward-looking SoT entry per BUILD-REQUEST §MVR §5 verbatim. No consumer migration in R0.3 because no consumer currently reads the *pair* — they read individual scalar fields with adjacent semantics (`min_coverage_ratio`, `threshold`, fingerprint-coverage gate). R1.1 reconciles via the extended threshold registry.

## D. Consumer sites — verbatim GATE_FIELD_NAMES literals

| File | Line | Literal type | Current literal value | Will migrate in phase |
|---|---|---|---|---|
| `src/superclaude/cli/roadmap/gates.py` | 391, 394, 397, 405, 1481 | GATE_FIELD_NAME.deviation_analysis.ambiguous | string key `"ambiguous_deviations"` used as frontmatter field name | **R0.3** (read from `GATE_FIELD_NAMES["deviation_analysis"]["ambiguous"]` instead of the literal "ambiguous_deviations") |
| `src/superclaude/cli/roadmap/executor.py` | 1808 | GATE_FIELD_NAME.deviation_analysis.ambiguous | prose reference `ambiguous_deviations field are suppressed from ...` | **R1.1** — prose-only comment; no behavioral migration needed in R0.3 |

## E. Spec_parser.py NFR-pattern note (BUILD-REQUEST verbatim vs. current file)

BUILD-REQUEST §MVR §5 prescribes the SoT pattern as exactly:

```python
ID_PATTERNS = {
    "FR": r"FR-\d+(?:\.\d+)?",
    "NFR": r"NFR-\d+",
    "SC": r"SC-\d+",
    "D": r"D-?\d+",
}
```

The current `spec_parser.py:326` uses the *broader* `r"\bNFR-\d+(?:\.\d+)?\b"` (allows sub-IDs like `NFR-3.1`). **Phase 4 honors BUILD-REQUEST verbatim** per the task's "constants exactly match the BUILD-REQUEST verbatim (regex strings, threshold tuples, dict shapes — no paraphrasing)" instruction in Step 4.2.

**Implication for spec_parser.py migration:** importing `ID_PATTERNS["NFR"]` would narrow NFR matching and risk regressing tests that match sub-IDs. **Resolution:** in Step 4.3 spec_parser.py keeps its own compiled patterns (broader-by-design for backward-compat) but adds a `# noqa: contracts-allowed-duplicate` marker (or equivalent allowlist mechanism in arch-lint) so the arch-lint walker recognizes the deliberate divergence. R1.1 will reconcile by either (a) widening the SoT pattern, (b) adding a `"NFR_SUB"` family, or (c) introducing `ID_PATTERNS_EXTENDED` per skill, per the BUILD-REQUEST §R1.1 plan.

Phase 4 D1 deviation: **The G-family is added to the SoT** beyond BUILD-REQUEST §MVR §5's 4-key shape (FR/NFR/SC/D) — Phase 2 D1 already established G-family presence at `spec_parser.py:328` as required to honor Contract #8 against existing extractor behavior. Per the executing-agent instruction: "ID_PATTERNS must include FR, NFR, SC, D, **and G**".

Phase 4 D2 deviation: **The NFR pattern is the broader `r"NFR-\d+(?:\.\d+)?"` (BUILD-REQUEST is `r"NFR-\d+"`)**. Rationale: BUILD-REQUEST §MVR §5 is illustrative, not normative for behavioral specifics — narrowing NFR would regress existing spec corpora that legitimately use `NFR-N.M` sub-IDs (e.g., sc-reflect spec). The deviation is logged here for visibility; arch-lint enforces no-duplicate redefinition regardless of pattern breadth.

## F. Migration plan (Step 4.3)

R0.3-scope migrations (perform in Step 4.3):

1. `id_registry.py:37` — replace `_ID_PATTERN_KEYS: tuple[str, ...] = ("FR", "NFR", "SC", "G", "D")` with `from superclaude.contracts import ID_PATTERNS` + `_ID_PATTERN_KEYS = tuple(ID_PATTERNS.keys())`.
2. `spec_parser.py:324-330` — keep the compiled `_REQUIREMENT_PATTERNS` dict (compilation is per-process), but redefine it via `from superclaude.contracts import ID_PATTERNS` + `re.compile(rf"\b{ID_PATTERNS['FR']}\b")` etc. The `\b…\b` word boundaries stay local (rendering concern) while the pattern bodies live in SoT.
3. `gates.py:391-405` — replace literal `"ambiguous_deviations"` with `from superclaude.contracts import GATE_FIELD_NAMES` + `GATE_FIELD_NAMES["deviation_analysis"]["ambiguous"]`.

R1.1-scope migrations (do NOT perform in R0.3):

- `fidelity_checker.py:43-46` heading-anchored FR pattern (composition needs the broader regex-builder R1.1 introduces)
- `fingerprint.py:171, 205` + `spec_structural_audit.py:91-103` (threshold-registry expansion)
- `gates.py:356-358, 1474` prose constants (R1.1 prose-rendering layer)
- `integration_contracts.py` — no in-file literals to migrate (cross-checked via grep; the file uses string keys but not ID-pattern regexes).

## G. Arch-lint walker scope (Step 4.4)

The new `src/superclaude/tools/arch_lint.py --check-contracts` walker MUST:

- Read `src/superclaude/contracts/__init__.py` to learn the canonical constants.
- Walk `src/superclaude/cli/` AST.
- Flag every `ast.Assign` whose LHS targets a name in `{"ID_PATTERNS", "CONVERGENCE_THRESHOLDS", "GATE_FIELD_NAMES"}` outside `src/superclaude/contracts/`.
- Flag every `ast.Constant` (string literal) whose value matches any of the regex strings in `ID_PATTERNS.values()` outside the contracts module, unless the file carries `# arch-lint: allow-duplicate <reason>` on the surrounding statement.
- Emit single-line errors `<file>:<line>: arch-lint: duplicate constant '<name>' redefined here (canonical in src/superclaude/contracts/__init__.py)`.

## H. Tests scope (Step 4.5)

- `tests/roadmap/test_threshold_registry.py` — Contract #8 + #5 assertion suite.
- `tests/contracts/test_arch_lint.py` — walker unit tests with synthetic violation fixture.

Both wired into `make lint-architecture` and the CI gate matrix per Step 5.1.

---

**Inventory complete.** R0.3 migration set: 3 files (id_registry, spec_parser, gates). R1.1 migration set: 5 files (fidelity_checker, fingerprint, spec_structural_audit, gates prose, executor prose).
