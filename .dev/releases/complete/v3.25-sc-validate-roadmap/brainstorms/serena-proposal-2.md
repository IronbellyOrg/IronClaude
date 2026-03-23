# Serena MCP Proposals D, E, F — Adversarial Review & Refactored Versions

## Adversarial Review Summary

### What Changed and Why

**Proposal D (Cross-Session Validation Ledger)**: Substantially reduced in scope. The core value — delta reporting between runs — survives, but adversarial calibration (using historical false-positive rates to tune Phase 4 intensity) was cut. The adversarial pass is a *fresh-eyes* review by design; injecting historical bias contradicts its purpose and violates the spirit of R3 (evidence-based claims from *this* run's evidence). The ledger write was moved from Phase 6 to a post-completion hook to avoid polluting the phase architecture with MCP side-effects. Serena availability must be gracefully optional throughout, not just as a footnote.

**Proposal E (Symbol-Graph Integration Verification)**: Rejected in its current form and replaced with a much narrower variant. The original proposal directly violates Section 8 Boundaries: "Will Not: Validate code execution or test results — only document-level coverage." Symbol graph traversal IS code-level validation. Additionally, Serena's `find_symbol` / `find_referencing_symbols` are NOT in the skill's `allowed-tools` list (`Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`). Adding Serena as a tool dependency changes the skill's contract. The refactored version uses existing allowed tools (Grep, Glob) to do lightweight symbol-existence checks, which captures 80% of the value without violating boundaries or adding tool dependencies.

**Proposal F (Progressive Domain Knowledge Accumulation)**: Cut by roughly 60%. Taxonomy persistence and correction memory were removed entirely. Taxonomy persistence creates a *consistency trap*: stable domains sound good but actually prevent the validator from adapting to genuinely changed architectures. Correction memory is dangerous — it lets past human errors suppress future valid findings, creating a silent accuracy degradation path. What survives is terminology persistence (genuinely useful, low-risk) and pattern recording (informational only, no behavioral changes). Both are scoped as strictly optional enrichments.

### Cross-Cutting Concerns

1. **allowed-tools violation**: None of these proposals can use Serena tools unless the skill's frontmatter `allowed-tools` is updated. This is a prerequisite, not an afterthought, and must be weighed against keeping the skill's tool surface small.
2. **Graceful degradation is non-negotiable**: Every Serena integration must be wrapped in try/fail-open logic. The validator must produce identical core output with or without Serena.
3. **Phase architecture purity**: The 7-phase pipeline (0-6) is well-defined with clear inputs/outputs. MCP side-effects (memory reads/writes) should be pre-phase and post-phase hooks, not injected into phase step logic.

---

# Serena MCP Proposal D (Refactored): Cross-Session Validation Ledger

## Problem Statement

The `sc-validate-roadmap-protocol` treats every invocation as stateless. When a user runs the validator, applies fixes, and reruns, the second run has no awareness of the first. This causes two concrete problems:

1. **Regression blindness**: A fix for GAP-C01 might break coverage for REQ-042, but the second run cannot flag this as a *regression* because it has no baseline.
2. **Remediation churn tracking is manual**: The user must visually diff two reports to determine which gaps closed, persisted, or are new. On a 200-requirement spec this is error-prone.

## Proposed Integration

Use Serena's `write_memory` / `read_memory` to maintain a **Validation Ledger** that persists across sessions. The integration is structured as **pre-phase and post-phase hooks** — not modifications to phase step logic.

**Pre-Phase 0 Hook — Load Baseline (optional, fail-open):**

1. Attempt `read_memory("validation-ledger/{roadmap-slug}/latest")`.
2. If found, parse into a baseline summary (verdict, coverage scores, gap ID list, requirement count).
3. If Serena unavailable or memory missing, proceed without baseline. No degradation to core validation.

**Post-Phase 6 Hook — Write Ledger Entry (optional, fail-open):**

1. After the Phase 6 summary artifact is written and the core validation is complete, write a ledger entry to `validation-ledger/{roadmap-slug}/{timestamp}`.
2. Write `validation-ledger/{roadmap-slug}/latest` pointing to the same entry.
3. If Serena unavailable, skip silently. The validation report is already on disk.

**Phase 3 Addition — Delta Section in Consolidated Report:**

During Step 3.10 (Write Consolidated Report), if a baseline was loaded, append a delta section:

- Gaps present in both runs: **PERSISTENT** (with run count if available).
- Gaps in previous but absent now: **RESOLVED**.
- Gaps absent in previous but present now: **NEW**.
- Requirements COVERED in previous but now PARTIAL/MISSING: **REGRESSION** (auto-escalate severity by one level).

This delta section is *informational* — it enriches the report but does not change how findings are adjudicated in Step 3.4.

## What Was Cut and Why

**Adversarial calibration was removed.** The original proposal used historical false-positive rates to tune Phase 4 challenge intensity. This contradicts the adversarial pass's fundamental design: it is a *fresh-eyes* review (Step 4.1 explicitly says "Do NOT rely on agent reports for this pass"). Injecting historical bias makes it less adversarial, not more effective. If past runs had low false-positive rates, that tells you the agents are good — it does NOT mean the adversarial pass should be more aggressive on this run's different content.

## Phase(s) Affected

- **Pre-Phase 0**: Load baseline (new hook, outside phase logic).
- **Phase 3, Step 3.10**: Append delta section to consolidated report (additive only).
- **Post-Phase 6**: Write ledger entry (new hook, outside phase logic).

## Implementation Sketch

```python
# Pre-Phase 0 hook — BEFORE document ingestion
baseline = None
try:
    raw = serena.read_memory(f"validation-ledger/{roadmap_slug}/latest")
    baseline = json.loads(raw.content) if raw else None
except Exception:
    baseline = None  # fail-open: proceed without baseline

# Phase 3, Step 3.10 — append to consolidated report (only if baseline exists)
if baseline:
    delta = compute_gap_delta(
        previous_gaps=baseline["gap_ids"],
        current_gaps=current_gap_registry,
    )
    append_delta_section(consolidated_report, delta)
    # Regressions get severity += 1 in the delta display,
    # but this does NOT retroactively change Step 3.4 adjudication.

# Post-Phase 6 hook — AFTER all artifacts are written
ledger_entry = {
    "timestamp": now_iso(),
    "verdict": verdict,
    "weighted_coverage": score,
    "gap_ids": {g.id: g.severity for g in gaps},
    "req_count": total_reqs,
    "spec_content_hash": hash_spec_files(spec_paths),
}
try:
    serena.write_memory(
        f"validation-ledger/{roadmap_slug}/{timestamp}",
        json.dumps(ledger_entry),
    )
    serena.write_memory(
        f"validation-ledger/{roadmap_slug}/latest",
        json.dumps(ledger_entry),
    )
except Exception:
    pass  # fail-open: validation is already complete
```

## Risks & Mitigations

- **Memory bloat**: Each entry is ~2-5 KB. Mitigation: prune entries older than 30 days or keep only last 10.
- **Slug collisions**: Mitigation: use full relative path as slug, normalized to filesystem-safe characters.
- **Stale baselines after spec changes**: Include `spec_content_hash` in ledger entry. If hash differs between runs, warn that delta is approximate due to spec changes.
- **Serena unavailable**: All ledger operations are fail-open. Core validation is identical with or without Serena.

---

# Serena MCP Proposal E (Refactored): Lightweight Symbol-Existence Checks

## Problem Statement

Phase 3, Step 3.7 (Integration Wiring Audit) validates integration points by matching prose descriptions. When a spec references specific code symbols (e.g., `PaymentProcessor.on_complete()`), the validator cannot check whether those symbols exist or have been renamed. This is a real gap — but the solution must stay within the skill's document-level boundaries.

## What Was Cut and Why

**The original proposal was rejected because it violates two hard constraints:**

1. **Section 8 Boundary Violation**: The skill explicitly declares "Will Not: Validate code execution or test results — only document-level coverage." Traversing a symbol graph via `find_symbol` and `find_referencing_symbols` is code-level analysis.

2. **allowed-tools Violation**: The skill's frontmatter lists `Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`. Serena tools (`find_symbol`, `get_symbols_overview`, `find_referencing_symbols`) are not in this list. Using them would be an execution rule violation.

3. **Scope creep**: The original proposal introduced fuzzy matching, reference graph traversal, and blast-radius analysis. Each of these is a feature-sized addition that moves the validator from "document audit" toward "code analysis tool."

## Refactored Proposal: Grep-Based Symbol Spot-Check

Use the skill's existing allowed tools (`Grep`, `Glob`) to perform lightweight symbol-existence checks. This captures the highest-value scenario (spec references a symbol that doesn't exist in the codebase) without crossing the document-level boundary.

**New optional sub-step in Phase 3, Step 3.7 — Symbol Spot-Check (--depth deep only):**

For each integration point where the spec text contains backtick-wrapped identifiers (the most reliable signal of a code symbol reference):

1. Extract backtick-wrapped identifiers from the spec requirement text.
2. Use `Grep` to search the codebase for each identifier.
3. If a symbol appears in zero files: flag as `symbol_not_found: true` on the integration entry. This upgrades an otherwise-COVERED integration to PARTIAL with a LOW finding: "Spec references symbol `X` which was not found in the codebase — verify it exists or has not been renamed."
4. If a symbol appears in files: note `symbol_found: true` with file paths. No further analysis.

This is a spot-check, not a graph analysis. It adds one `Grep` call per backtick-wrapped symbol, bounded by the number of integration points (typically 5-30).

## Phase(s) Affected

- **Phase 3, Step 3.7**: Optional enrichment of integration entries with `symbol_found` / `symbol_not_found` flags. Only for `--depth deep`.

## Implementation Sketch

```python
# Phase 3, Step 3.7 — only for --depth deep
if depth == "deep":
    for integration in integration_points:
        backtick_symbols = re.findall(r'`([A-Za-z_]\w*(?:\.\w+)*)`', integration.spec_text)
        for sym in backtick_symbols:
            # Use Grep (allowed tool) to search codebase
            results = grep(pattern=sym, path=project_root, type="py")
            if not results:
                integration.symbol_evidence.append({
                    "symbol": sym,
                    "status": "NOT_FOUND_IN_CODEBASE",
                })
                # Downgrade to PARTIAL if was COVERED
                if integration.verdict == "FULLY_WIRED":
                    integration.verdict = "PARTIALLY_WIRED"
                    add_finding(
                        severity="LOW",
                        description=f"Spec references `{sym}` but symbol not found in codebase",
                    )
```

## Risks & Mitigations

- **False positives from grep**: A symbol name like `run` will match everywhere. Mitigation: only check backtick-wrapped identifiers with dot-notation or PascalCase/snake_case patterns longer than 6 characters.
- **Language limitations**: Grep is language-agnostic but imprecise. Mitigation: this is a spot-check, not a guarantee. Findings are LOW severity and informational.
- **Performance**: One grep per symbol. For 30 integration points averaging 2 symbols each, that is 60 grep calls. Acceptable for `--depth deep`.

---

# Serena MCP Proposal F (Refactored): Terminology Persistence

## Problem Statement

The validator builds domain context from scratch on every run. For teams that validate related roadmaps repeatedly, two things are wastefully re-derived:

1. **Project-specific terminology**: Terms like "TurnLedger" or "fidelity gate" have project-specific meanings that the validator must re-derive from context each time.
2. **Recurring patterns**: Certain requirement types are consistently PARTIAL across runs, suggesting systematic under-specification — but this insight evaporates between sessions.

## What Was Cut and Why

**Taxonomy persistence was removed.** The original proposal persisted domain boundaries across runs for "consistency." This creates a *consistency trap*: if a project's architecture changes between v1.0 and v3.0, stale domain boundaries actively harm extraction accuracy. The validator's cold-start domain clustering (Step 0.4) is designed to adapt to the *current* spec — seeding it with stale domains biases it toward the past. Cross-run domain comparison can be done post-hoc by the user reading reports side-by-side; it does not need to be enforced by the tool.

**Correction memory was removed.** This is the highest-risk item in the original proposal. It allows a user's past disagreements with findings to automatically suppress future findings. If a user incorrectly rejects a valid finding, the correction memory silently degrades future accuracy. The expiration mechanism (5 runs / 60 days) does not help — the damage occurs within those 5 runs. Additionally, automated severity adjustment based on past corrections violates R3 (evidence-based claims) and R4 (spec is source of truth) — findings should be adjudicated based on current evidence, not historical user preferences.

**Agent assignment optimization was removed.** "Optimal agent configurations" from past runs presuppose that the same domains and requirement distributions apply to the next run. This is rarely true for evolving projects.

## Refactored Proposal: Terminology Map + Pattern Log

Two lightweight, low-risk Serena memory integrations:

### Terminology Map (Pre-Phase 0 load, Post-Phase 6 write)

**Load**: At startup, attempt `read_memory("project-terms/{project-slug}")`. If found, make the term map available during Phase 0, Step 0.2 requirement extraction. Terms are used as context hints, not as overrides — the validator still extracts from the current spec text.

**Write**: After Phase 6, if new glossary terms were discovered during extraction (from spec glossary sections, defined terms, or `NEEDS-SPEC-DECISION` resolutions), merge them into the term map and persist.

**Content**: A simple dictionary mapping project-specific terms to plain-language definitions. Maximum 200 entries. Example: `{"TurnLedger": "audit log system", "fidelity gate": "quality checkpoint"}`.

**Behavioral constraint**: The terminology map is *advisory*. It helps the extractor resolve ambiguous text but does not change coverage assessments, finding severity, or verdicts. If the map says "fidelity gate = quality checkpoint" but the current spec defines it differently, the current spec wins (R4).

### Pattern Log (Post-Phase 6 write only)

**Write only** — this is a log, not a feedback loop. After Phase 6, record:

- Requirement types that are consistently PARTIAL (suggests systematic under-specification in roadmap format).
- Domains with consistently high gap rates.
- Total requirement count and coverage score for trend tracking.

**No behavioral impact**: The pattern log does NOT change how any phase operates. It is written to `project-patterns/{project-slug}` for human review during retrospectives. A user can read it via `read_memory` in a separate session to understand trends, but the validator never loads it during execution.

This is the key distinction from the original proposal: patterns are recorded for human consumption, not consumed by the validator to change its behavior.

## Phase(s) Affected

- **Pre-Phase 0**: Load terminology map (fail-open).
- **Phase 0, Step 0.2**: Use terminology map as extraction context hints.
- **Post-Phase 6**: Write updated terminology map and pattern log entry.

## Implementation Sketch

```python
# Pre-Phase 0 hook
term_map = {}
try:
    raw = serena.read_memory(f"project-terms/{project_slug}")
    term_map = json.loads(raw.content) if raw else {}
except Exception:
    term_map = {}  # fail-open

# Phase 0, Step 0.2 — terminology as context hints during extraction
# term_map is passed to the requirement extractor as advisory context
# e.g., when spec says "TurnLedger", extractor knows it means "audit log system"
# This helps with domain classification, NOT with coverage assessment

# Post-Phase 6 hook — persist terminology
new_terms = extract_glossary_terms(spec_files)
if new_terms:
    merged = {**term_map, **new_terms}
    # Cap at 200 entries, keep most recent
    if len(merged) > 200:
        merged = dict(list(merged.items())[-200:])
    try:
        serena.write_memory(
            f"project-terms/{project_slug}",
            json.dumps(merged),
        )
    except Exception:
        pass  # fail-open

# Post-Phase 6 hook — write pattern log (append-only, never read by validator)
pattern_entry = {
    "timestamp": now_iso(),
    "roadmap": roadmap_path,
    "req_count": total_reqs,
    "weighted_coverage": score,
    "verdict": verdict,
    "consistently_partial_types": [
        t for t, rate in type_partial_rates.items() if rate > 0.5
    ],
    "high_gap_domains": [
        d for d, rate in domain_gap_rates.items() if rate > 0.3
    ],
}
try:
    existing = serena.read_memory(f"project-patterns/{project_slug}")
    patterns = json.loads(existing.content) if existing else []
    patterns.append(pattern_entry)
    patterns = patterns[-20:]  # keep last 20
    serena.write_memory(
        f"project-patterns/{project_slug}",
        json.dumps(patterns),
    )
except Exception:
    pass  # fail-open
```

## Risks & Mitigations

- **Stale terminology**: A term definition from v1.0 may mislead on v3.0. Mitigation: current spec definitions always override the map (R4). Include `last_updated` timestamp; terms older than 90 days are treated as lower-confidence hints.
- **Serena unavailable**: All operations are fail-open. Validator behavior is identical without Serena — slightly less context during extraction, no pattern log written.
- **Cross-project contamination**: Derive project slug from git remote URL or user-specified `--project` flag, not directory name alone.
- **Pattern log size**: Capped at 20 entries. Each entry is ~500 bytes.
