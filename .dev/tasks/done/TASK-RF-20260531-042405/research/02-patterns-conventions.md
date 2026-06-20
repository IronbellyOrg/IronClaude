# Researcher R2 — Patterns & Conventions (Current Pipeline)

**Date:** 2026-05-31
**Worktree root:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/`
**Scope:** Six representative pipeline files plus the shared `cli/pipeline/models.py` base.
**Citations:** All file:line references are against the worktree paths above; line numbers verified via Read.

---

## 1. `cli/roadmap/executor.py` — Pipeline orchestrator

### 1.1 `_build_steps` step assembly (L1947)

Signature:

```python
def _build_steps(config: RoadmapConfig) -> list[Step | list[Step]]:
```

`executor.py:1947-1953`. Returns a heterogeneous list where each element is either a single `Step` (sequential) or `list[Step]` (parallel group). The hand-rolled list literal spans L2000–L2222 with **11 logical steps**, each constructed directly inline. The numbered step comments embedded in the file (`# Step 1: Extract`, `# Step 2`, …, `# Step 11: Remediate`) mis-number internally — there are two `# Step 8` entries (Test Strategy at L2139 and Spec Fidelity at L2157) — so the spec's "≤14 steps" budget (Contract #2) is **already approached on its current count, and the step IDs/labels do not match the comment numbering**. R1 must replace this hand-rolled list with a contract-checked registry.

Step IDs used (verified strings in the file):
- `extract` (L2004)
- `generate-{agent_a.id}` / `generate-{agent_b.id}` parallel group (L2031, L2049)
- `diff` (L2069)
- `debate` (L2079)
- `score` (L2089)
- `merge` (L2108)
- `anti-instinct` (L2131) — non-LLM deterministic
- `test-strategy` (L2141)
- `spec-fidelity` (L2159)
- `wiring-verification` (L2176) — `gate_mode=GateMode.TRAILING`
- `deviation-analysis` (L2187) — non-LLM
- `remediate` (L2197) — non-LLM

That is **12 steps in the visible slice** (extract+2×generate+diff+debate+score+merge+anti-instinct+test-strategy+spec-fidelity+wiring-verification+deviation-analysis+remediate), and the file continues past L2200 with at least one more (`certify` from `build_certify_step` at L1899). Contract #2's "step count ≤14" is **already marginal** and the registry-based replacement must enforce it programmatically.

### 1.2 `gate=None` bypass at L2167 (Contract #4 target)

```python
gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE,
```

`executor.py:2167`. This is the **single explicit `gate=None` bypass** in `_build_steps`. When convergence mode is on (the default per `commands.py:188` / `--no-convergence` flag), the spec-fidelity step writes its file but has **no GateCriteria attached**, so its output is unverified before the next step consumes it. Contract #4 mandates that empty-target outputs must explicitly fail — this is exactly the construct that must be eliminated.

Other `return True` paths in `executor.py` that look like bypasses but are NOT gate=None patterns:
- L2465, L2506, L3380, L3480 — these are local function early returns (cache hit, resume-state checks), not gate skips.
- L3313 — `# Cycle was attempted but failed — don't retry` — control-flow short-circuit, not fragility.
- L3324 — same pattern (control-flow).
- L3563, L3568, L3595, L3598 — tuple returns from a `_should_rerun` helper; second element is a reason string. These are explicit decisions, not stubs.

**Net `gate=None` bypass count in `_build_steps`: exactly 1 (L2167).** Contract #4 work is therefore surgical, not sweeping.

### 1.3 `build_certify_step` (L1899)

```python
def build_certify_step(
    config: RoadmapConfig,
    findings: list | None = None,
    context_sections: dict[str, str] | None = None,
    remediation_summary: list[str] | None = None,
) -> Step:
```

`executor.py:1899-1944`. Returns a `Step` with `id="certify"`, `gate=CERTIFY_GATE`, `timeout_seconds=300`, and `retry_limit=1`. Notable: **the certify step is built by a separate function**, not appended to `_build_steps`'s list. This means R1.3's `GateCriteria.code_assertions` slot has to either (a) be attached at the `CERTIFY_GATE` definition (in `gates.py`) or (b) be threaded through `build_certify_step` as a new parameter. The current factory-function pattern is the simplest hook point for R1.3 wiring.

---

## 2. `cli/roadmap/gates.py` — Gate registry + semantic checks

### 2.1 `SemanticCheck` signature inheritance from `pipeline.models`

```python
from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck
```

`gates.py:25`. The concrete dataclass lives in `cli/pipeline/models.py:82-87`:

```python
@dataclass
class SemanticCheck:
    """Pure Python check applied to file content. No LLM invocation."""
    name: str
    check_fn: Callable[[str], bool | str]
    failure_message: str
```

This is the **inherent flaw per Vector A**: `check_fn: Callable[[str], bool | str]` takes **only** file content and returns **only** bool/str. There is **no slot for**:
- a `CodeAssertion` (cross-file AST link),
- access to the spec ID set,
- access to the pipeline envelope (cross-step state),
- access to the working tree.

Every gate is therefore confined to validating its **own file in isolation** — no gate can express "the function named in this roadmap exists in the codebase." Contract #3/R1.3 requires extending this dataclass with a `code_assertions: list[CodeAssertion] | None` slot (or augmenting `GateCriteria` directly at L91-105 in `models.py`).

### 2.2 `GateCriteria` dataclass (models.py:91-105, used throughout gates.py:317-383+)

```python
@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str | tuple[str, ...]]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
```

The four-tier enforcement model (`EXEMPT`/`LIGHT`/`STANDARD`/`STRICT`) is dispatched in `cli/pipeline/gates.py:20-76` (`gate_passed`). All `GateCriteria` instances in `gates.py:1020-1273` (EXTRACT_GATE, EXTRACT_TDD_GATE, GENERATE_A_GATE, GENERATE_B_GATE, DIFF_GATE, DEBATE_GATE, SCORE_GATE, MERGE_GATE, TEST_STRATEGY_GATE, SPEC_FIDELITY_GATE, and more later in the file) are module-level constants — pure data with no logic, per the docstring at L1-10. **Pattern to preserve**: gates are data, not behavior.

### 2.3 `_cross_refs_resolve` stub (L48-91, Contract #5 target)

```python
def _cross_refs_resolve(content: str) -> bool:
    ...
    if unresolved:
        for ref in unresolved:
            warnings.warn(
                f"Unresolved cross-reference: 'See section {ref}' has no matching heading",
                stacklevel=2,
            )
        # Warning-only mode (OQ-001): return True to avoid blocking pipeline
        return True
    return True
```

`gates.py:48-91`. The function returns `True` in **both** the unresolved-references branch (after emitting `warnings.warn`) **and** the all-resolved branch — the function is **structurally incapable of returning False**. Comment at L88 ("Warning-only mode (OQ-001): return True to avoid blocking pipeline") explicitly documents this as intentional fragility. Used by `MERGE_GATE` at L1188-1192. **This is the canonical Contract #5 stub** — its public contract says "validate" but its implementation guarantees PASS. R1.6 must delete this and either wire it to actually fail-closed on unresolved refs or remove the SemanticCheck entry from MERGE_GATE entirely.

### 2.4 `_parse_frontmatter` variant #1 (gates.py:168-189)

```python
def _parse_frontmatter(content: str) -> dict[str, str] | None:
    """Extract YAML frontmatter key-value pairs from content.
    Returns a dict of key→value strings, or None if no frontmatter found.
    """
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return None
    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return None
    result: dict[str, str] = {}
    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = _strip_yaml_quotes(value.strip())
    return result
```

`gates.py:168-189`. Used by **26 semantic-check functions** in `gates.py` (every `fm = _parse_frontmatter(content)` line — verified at L133, 203, 282, 323, 341, 359, 373, 399, 422, 439, 460, 483 (return), 497, 532, 564, 609, 632, 661, 678, 696, 720, 735 (return), 743, 756, 790). Returns `dict[str, str]`. Requires frontmatter to be at the **very start** of the file (`stripped.startswith("---")`).

### 2.5 `_check_frontmatter` variant #2 (pipeline/gates.py:91-142)

```python
# cli/pipeline/gates.py:91
def _check_frontmatter(
    content: str,
    required_fields: list[str | tuple[str, ...]],
    output_file: Path,
) -> tuple[bool, str | None]:
    ...
    frontmatter_text: str | None = None
    for match in _FRONTMATTER_RE.finditer(content):
        body = match.group(1)
        if _TOPLEVEL_KEY_RE.search(body):
            frontmatter_text = body
            break
    ...
```

`cli/pipeline/gates.py:91-142`, with module-level regexes at L79-88:

```python
_FRONTMATTER_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*$", re.MULTILINE | re.DOTALL)
_TOPLEVEL_KEY_RE = re.compile(r"^([A-Za-z_][\w\-]*)\s*:", re.MULTILINE)
```

**Contract #6 divergence (verbatim disagreement table):**

| Behavior | `gates._parse_frontmatter` (L168-189) | `pipeline.gates._check_frontmatter` (L91-142) |
|---|---|---|
| Position of `---` | MUST be at file start (`content.lstrip().startswith("---")`) | Can appear after preamble — `re.finditer` walks every delimiter pair |
| Multiple `---` pairs | Stops at first `\n---` after start | Iterates all, picks first body containing a top-level key |
| Horizontal-rule rejection | None — any `---…\n---` is treated as frontmatter | Yes — `_TOPLEVEL_KEY_RE.search(body)` filters out empty/HR pairs |
| Quoted-value handling | Uses `_strip_yaml_quotes` to strip outer matched quotes | No quote stripping — keys-only check |
| Nested list values (`  - id: M1`) | Captured as `dict[key, value]` with same flat shape — would mis-key | Tolerated — only top-level keys via `^([A-Za-z_]...)` anchor |
| Return shape | `dict[str, str] \| None` | `tuple[bool, str \| None]` — gate-style |
| Consumers | 26 semantic checks inside `gates.py` | Single caller: `gate_passed` STANDARD/STRICT path at `pipeline/gates.py:54-59` |

A roadmap output containing CONV-comment preamble before its YAML frontmatter would PASS the pipeline-level frontmatter check but FAIL every roadmap-level semantic check (because `_parse_frontmatter` returns `None` and all 26 callsites then return False). This is **the exact Contract #6 split-personality bug** — both parsers exist, both are called in sequence on the same file, and they disagree on what "has frontmatter" means.

### 2.6 `_REQUIRED_H2_SECTIONS` and `_normalize_heading` (gates.py:891, 919)

Shared with `obligation_scanner.py` via direct import at `obligation_scanner.py:21-26`:

```python
from superclaude.cli.roadmap.gates import (  # noqa: E402
    _REQUIRED_H2_SECTIONS as _TAIL_SECTION_HEADINGS,
)
from superclaude.cli.roadmap.gates import (  # noqa: E402
    _normalize_heading,
)
```

Comment at obligation_scanner.py:18-20 explicitly calls this out: "Tail-section headings — MUST stay in sync with gates._REQUIRED_H2_SECTIONS. Imported at module load to avoid drift; no circular-import risk because gates.py does not import obligation_scanner." This is the **current SoT pattern for shared template/section constants** — a candidate for migration to `superclaude.contracts` per MVR §5.

---

## 3. `cli/roadmap/fidelity_checker.py` — Fail-open default (Contract #4 / R1.6 target)

### 3.1 Fail-open at L287-303

```python
for mapping in mappings:
    if not mapping.expected_names:
        # No extractable names for this FR — ambiguous, fail-open
        logger.warning(
            "FR %s: no function/class names extracted from spec; "
            "marking as ambiguous (fail-open per R-3)",
            mapping.fr_id,
        )
        results.append(
            FidelityResult(
                fr_id=mapping.fr_id,
                found=True,  # fail-open
                ambiguous=True,
                message=f"No extractable names for {mapping.fr_id}; fail-open",
            )
        )
        continue
```

`fidelity_checker.py:287-303`. **Comment at L298 (`found=True,  # fail-open`) is the smoking gun** — when the checker cannot extract names from a spec FR (e.g., the FR is prose-only with no code identifiers), it records the FR as *found*. This is the direct ancestor of multiple recurrence-corpus FPs per master:§Flaw 4: a spec FR that says "the system MUST validate user credentials" with no code names gets stamped `found=True` even though zero codebase evidence was searched.

A second fail-open at L317-323:

```python
if evidence:
    found = True
    if missing:
        logger.warning(
            "FR %s: partial evidence — found %s, missing %s; "
            "marking as found (fail-open per R-3)",
            ...
        )
```

`fidelity_checker.py:314-337`. When **any** name in `expected_names` matches the codebase, the FR is marked `found=True` even if most expected names are missing. The `ambiguous=bool(missing)` flag is set but consumers downstream (the spec-fidelity prompt builder, the deviation-analysis step) treat `found=True` as "pass" regardless. **Contract #4 target**: replace both fail-open returns with explicit ambiguous/unknown disposition that surfaces as a HIGH finding rather than a silent pass.

### 3.2 R1.5 wiring target: `check_as_findings` (L355+)

The function exposing fidelity gaps as `Finding` objects for the convergence registry is at `fidelity_checker.py:355`. R1.5's `verify-implementation` terminal step would replace the fail-open results paths with AST-grounded `CodeAssertion` lookups (per R1.3 slot), removing both fail-open branches and instead emitting structured "AST search returned no symbol" findings.

---

## 4. `cli/roadmap/obligation_scanner.py` — Layer 1-5 detectors

### 4.1 Layer-by-layer structure

The scanner is a **5-layer cascade** of meta-context detectors before a scaffold-term match is promoted to a HIGH obligation. Each layer is documented inline:

- **Layer 1a — Inline-code scaffold** (`obligation_scanner.py:41-45`):
  ```python
  _INLINE_CODE_SCAFFOLD_RE = re.compile(
      r"`[^`]*(?:" + "|".join(SCAFFOLD_TERMS) + r")[^`]*`",
      re.IGNORECASE,
  )
  ```
- **Layer 1b — Completed checklist** (`obligation_scanner.py:47-48`): `_COMPLETED_CHECKLIST_RE = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE)`
- **Layer 2 — Negation/meta-context prefix** (`obligation_scanner.py:50-64`): regex covering "no/not/never/without/ensure no/verify no/check (for) no/must not/should not/shall not/cannot/don't/reject/prohibit/forbid/prevent/disallow" plus past-tense removal verbs plus risk/warning/caution/danger/caveat/concern prefixes plus "verification/gate criteria/check (for/that)/validate/assert/audit" hits. (Also shell-cmd and risk/warning sub-detectors at L66-82.)
- **Layer 3a — Imperative table-cell** (`obligation_scanner.py:84-91`): `r"^\s*\|[^|]*\|\s*scaffold\s+\w+"` — narrow to *scaffold* only, because mock/stub/fake/dummy in table cells are genuine obligations.
- **Layer 3 (Stage 2) — Table separator filter** (`obligation_scanner.py:93-100`): only separator rows (`|---|---|`) skip; data rows now reach Layer 3a/3b. The prior `stripped_context.startswith("|")` guard at `scan_obligations` collapsed both into `continue` — comment at L97-99 documents this as the bug Fix 3 corrected.
- **Layer 3b — Parenthetical phase label** (`obligation_scanner.py:151-159`): bracketed multi-word labels like `(command scaffolding)` or `(Phase 2 mocking)` demote; bare `(scaffold)` stays HIGH.
- **Layer 4 — Descriptor-noun adjacency** (`obligation_scanner.py:102-129`): scaffold terms next to nouns from the frozenset `{outcome, result, behavior, behaviour, property, mitigation, fallback, dependency, consideration, historical, legacy, prior, existing}` demote *unless* the line also matches discharge intent.
- **Layer 5 — H3 subsection demotion** (`obligation_scanner.py:131-149`): scaffold-term findings inside H3 sections whose lowercased heading starts with one of `("risk assessment", "integration points", "milestone dependencies", "open questions")` demote from HIGH to MEDIUM, *unless* the line itself matches discharge intent.

### 4.2 Recurrence #6 ancestry

The MultiModelSwarm FP per master:§Recurrence#6 maps to a real scaffold-term match in a roadmap section that the Layer 4 descriptor-noun demoter or Layer 5 H3 demoter did not catch (or, conversely, where a legitimate obligation was demoted because of overlap with a descriptor noun). R0.2's vocab-lint allowlist must extend either `_DESCRIPTOR_NOUNS` (L109-125) or `_DEMOTED_H3_SUBSECTIONS` (L137-142) with case-specific entries — both registries are currently inline literals in `obligation_scanner.py`, not in any shared `contracts` module. R0.3 moves them to `superclaude.contracts.vocabulary` per MVR §5.

### 4.3 Convention takeaways

- `SCAFFOLD_TERMS` and `DISCHARGE_TERMS` live in `superclaude.cli.vocabulary` (imported at `obligation_scanner.py:27`) — that module already exists as a shared SoT for scanner vocab. R0.3 should follow this pattern when creating `superclaude.contracts` rather than inventing a new module shape.
- All layer detectors are **module-level pre-compiled regexes** with verbose docstrings — preserve this style. The R1 rewrite should keep these inline rather than moving them to YAML/JSON, because the embedded edge-case rationale (e.g., L84-91 "scaffold as verb in table cell — narrow to scaffold only") is dense and load-bearing.

---

## 5. `cli/roadmap/convergence.py` — PRESERVE target

### 5.1 What "preserve" means concretely

The MVR (Vector A) lists `convergence.py` as preserve. The stable API surface that R1 must NOT break:

- **Module-level cost constants** (`convergence.py:26-34`): `CHECKER_COST = 10`, `REMEDIATION_COST = 8`, `REGRESSION_VALIDATION_COST = 15`, `CONVERGENCE_PASS_CREDIT = 5`, `MIN/STD/MAX_CONVERGENCE_BUDGET = 28/46/61`. Other modules read these directly — moving them breaks `sprint/models.py`'s `TurnLedger` callers.
- **`reimburse_for_progress(ledger, prev_structural_highs, curr_structural_highs) -> int`** (L44-60): public credit-reimbursement function called from the executor's convergence loop. Signature must remain stable.
- **`compute_stable_id(dimension, rule_id, spec_location, mismatch_type) -> str`** (L63-71): SHA256-based deterministic finding ID. Other modules (`fidelity_checker.py:368` calls this) depend on the exact hash output — changing the input string format would invalidate all existing `.roadmap-state.json` finding IDs across all in-progress release dirs.
- **Dataclasses** (`RunMetadata` L74, `DeviationRegistry` L90, `ConvergenceResult` L320, `RegressionResult` L333): public schemas, persisted to JSON. R1 envelope migration must dual-write rather than replace.
- **`execute_fidelity_with_convergence(...)`** (L434): the top-level entry point. Signature has 8 parameters with sensible defaults — preserve all of them. R1.5's verify-implementation step can be added as a new callable wired into the `run_checkers` callback, not by changing this function's signature.
- **`handle_regression(...)`** (L671): regression handler. Preserve.
- **`_check_regression`** (L343-378): private but stable — drives the FR-8 contract that **only structural HIGH increases trigger regression** (semantic fluctuations are logged warnings only). This is a contract the recurrence corpus encodes; do not "fix" it without an explicit Contract update.
- **`atexit.register(_atexit_cleanup)`** (L431): module-import side effect for tmpdir cleanup. R1 envelope work must not break this — if the envelope moves to a different cleanup model, the atexit registration must still fire OR be replaced with an equivalent guard.

### 5.2 The "wrapper pattern" to preserve

`convergence.py` is structured as a **side-effect-free coordination layer** over caller-supplied callbacks (`run_checkers`, `run_remediation`, `handle_regression_fn` parameters of `execute_fidelity_with_convergence`). R1's envelope work should keep this wrapper shape — the envelope becomes the *input* the callbacks read, not a change to the convergence loop's control flow.

---

## 6. `cli/roadmap/commands.py` — PRESERVE target (Click CLI surface)

### 6.1 Public CLI surface (preserve verbatim)

`@click.group("roadmap")` at L14 defines the `superclaude roadmap` command group. The three subcommands plus their options are the user-visible contract:

- **`superclaude roadmap run`** (`commands.py:32-298`) — primary entry. **20 options**, every one of which is documented in help text and consumed by downstream code:
  - `--agents`, `--output`, `--depth` (L36-56)
  - `--resume`, `--dry-run` (L57-69)
  - `--model`, `--max-turns` (L70-80)
  - `--debug`, `--no-validate` (L81-90)
  - `--allow-regeneration`, `--no-convergence` (L91-102)
  - `--retrospective` (L103-112)
  - `--input-type`, `--tdd-file`, `--prd-file` (L113-140)
  - `--no-compress` (L141-151)
  - `--allow-cosmetic-remediation`/`--no-allow-cosmetic-remediation` (L152-162)
  - `--strict-no-remediation` (L163-173)
  - Positional `input_files` (1-3 files, `nargs=-1`, L33-35)

- **`superclaude roadmap accept-spec-change`** (`commands.py:301-324`) — single positional `output_dir`. Calls into `spec_patch.prompt_accept_spec_change`. Preserve.

- **`superclaude roadmap validate`** (`commands.py:327-353`) — `output_dir` + `--agents`, `--model`, `--max-turns`, `--debug`. Preserve.

### 6.2 Convergence-default contract

`commands.py:188` declares `--no-convergence` with `default=False`, so `convergence_enabled = not no_convergence` evaluates to **True by default**. This is the upstream cause of the `gate=None` bypass at `executor.py:2167` firing on virtually every real run — convergence is the production path, so spec-fidelity has no gate on production. R1.6's deletion of the bypass must coincide with the SPEC_FIDELITY_GATE being made convergence-aware (e.g., by passing the convergence registry into a `CodeAssertion`-bearing variant of the gate).

### 6.3 What "preserve" means here

The CLI surface — exact option names, exact flag-vs-arg shape, exact help text — is the **user-facing contract**. R1 may add options (e.g., a new `--envelope-mode` for dual-write toggling) but **must not rename or remove** any of the 20 existing `run` options or the two subcommands. Help text is part of the contract (script automation and shell completion scrape it). Defaults are part of the contract (`--no-convergence default=False` is load-bearing).

---

## 7. Cross-cutting convention summary

### Conventions to keep in the R1 rewrite

1. **Gates are pure data** (`gates.py:1018+`, `models.py:91`). New gates added during R1 must be module-level `GateCriteria` instances, not factory functions returning ad-hoc gates. (`build_certify_step` is the exception that proves the rule — and even there, the `gate=CERTIFY_GATE` reference is to a module constant.)
2. **Step IDs are kebab-case strings** (`extract`, `generate-{agent.id}`, `anti-instinct`, `wiring-verification`, `deviation-analysis`). New steps follow this.
3. **Parallel groups are `list[Step]` inside the step list**, not a wrapper dataclass (`executor.py:2029-2066`). Preserve.
4. **Non-LLM deterministic steps set `prompt=""`** with a comment explaining (`executor.py:2132, 2188, 2198`). Preserve.
5. **Cross-module constants live in shared modules** — `vocabulary.py` for scaffold/discharge terms, `gates._REQUIRED_H2_SECTIONS` for required headings. R0.3's `superclaude.contracts` follows this same pattern; do not invent a new layout.
6. **`@dataclass` for all step/result/registry models** (`models.py:82,91,109,126`, `convergence.py:74,90,320,333`). Preserve.

### Anti-patterns to remove in the R1 rewrite

1. **Hand-rolled step lists** (`executor.py:2000-2222`). Replace with a registered step-table that a contract check can iterate.
2. **`gate=None` bypasses** (`executor.py:2167`). Contract #4 — every step must have a gate; "no validation needed" is expressed as an EXEMPT-tier gate, not `None`.
3. **`return True` semantic-check stubs** (`gates.py:48-91`). Contract #5 — every semantic check must have a path to `False`. CI lint enforces.
4. **Duplicate frontmatter parsers** (`gates.py:168` vs `pipeline/gates.py:91`). Contract #6 — exactly one canonical parser, exported from a single module, both consumers import.
5. **Fail-open defaults** (`fidelity_checker.py:287-303, 314-337`). Contract #4 — ambiguity surfaces as a HIGH finding, not a silent PASS.
6. **`SemanticCheck.check_fn: Callable[[str], bool | str]` shape** (`models.py:82-87`). R1.3 — add a `code_assertions` slot so checks can reach beyond the single output file.

### Naming conventions observed

- Gate constants: `SCREAMING_SNAKE_CASE_GATE` suffix (`EXTRACT_GATE`, `MERGE_GATE`).
- Semantic check functions: `_lowercase_with_leading_underscore` (`_no_heading_gaps`, `_cross_refs_resolve`).
- Step builders: `build_<step>_step` (`build_certify_step`); LLM-prompt builders: `build_<step>_prompt` (`build_extract_prompt`, etc., from `prompts.py`).
- Module-level regexes: `_UPPER_SNAKE_RE` (`_FRONTMATTER_RE`, `_TOPLEVEL_KEY_RE`, `_SCAFFOLD_RE`, `_DISCHARGE_RE`, `_TABLE_SEPARATOR_RE`).
- Dataclasses for findings/registries: `PascalCase` (`Obligation`, `ObligationReport`, `DeviationRegistry`, `RunMetadata`, `ConvergenceResult`).

R1 must follow these conventions when introducing new types (`PipelineEnvelope`, `CodeAssertion`, etc.).

---

## 8. R0/R1 file-touch matrix derived from this evidence

| Symbol / location | R0 phase | R1 phase | Action |
|---|---|---|---|
| `gates.py:48-91` `_cross_refs_resolve` | — | R1.6 | Delete or make fail-closed |
| `executor.py:2167` `gate=None` ternary | — | R1.6 | Replace with convergence-aware SPEC_FIDELITY_GATE |
| `fidelity_checker.py:287-303` fail-open | — | R1.6 | Replace with ambiguous-as-HIGH |
| `fidelity_checker.py:314-337` partial-match fail-open | — | R1.6 | Same |
| `models.py:82-87` `SemanticCheck` shape | — | R1.3 | Add `code_assertions: list[CodeAssertion] \| None` |
| `models.py:91-105` `GateCriteria` shape | — | R1.3 | Add `code_assertions` slot OR change `SemanticCheck` |
| `gates.py:168` `_parse_frontmatter` | — | R1.6 | Delete; replace callsites with canonical parser |
| `pipeline/gates.py:91` `_check_frontmatter` | — | R1.6 | Promote to canonical, export from contracts |
| `obligation_scanner.py:109-125` `_DESCRIPTOR_NOUNS` | R0.2 | — | Extend with vocab-lint allowlist entries |
| `obligation_scanner.py:137-142` `_DEMOTED_H3_SUBSECTIONS` | R0.2 | — | Extend if recurrence corpus requires |
| `executor.py:1899-1944` `build_certify_step` | — | R1.3 | Wire `CodeAssertion` for certify gate |
| `executor.py:1947-2222` `_build_steps` | — | R1.2 | Replace list literal with envelope-aware registry |
| `convergence.py` entire module | — | R1 (envelope-migration touch only) | Preserve all public API |
| `commands.py` entire module | — | R1 (no functional changes; help text may evolve) | Preserve all flags |

End of R2 findings.
