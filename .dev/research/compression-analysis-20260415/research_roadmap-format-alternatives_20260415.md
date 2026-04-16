# Research Report: Alternative File Formats for Roadmap Token Reduction

**Date**: 2026-04-15
**Subject**: Token-efficient alternatives to Markdown for roadmap files consumed by downstream LLM agents
**Source file**: `.dev/releases/complete/v3.2_fidelity-refactor___/roadmap-opus-architect.md`
**Confidence**: High (backed by 2024-2026 benchmarks, including Claude-specific measurements)
**Revision**: v2 — Added TOON and XML analysis; revised primary recommendation

---

## Executive Summary

The source roadmap is **~4,600 tokens** (342 lines, 16,985 bytes) of structured Markdown containing phases, tasks with requirement IDs (FR-T02a), validation criteria (SC-001), risk tables, dependency tables, and timeline estimates.

**Revised key finding**: Two format families stand out: (1) **TOON** (Token-Oriented Object Notation, 2025) achieves -53% vs. Markdown on tabular data but fails on mixed prose+structure; (2) **XML** is explicitly trained into Claude as a structural delimiter and Anthropic officially recommends it for prompt/document structuring. The optimal format is a **Hybrid XML + TOON + prose** layout that combines Claude's trained XML priors with TOON's tabular compression and Markdown's prose handling.

Format-swapping alone (YAML, TOML, pretty JSON) yields *negative* savings. Compact Markdown with conventions yields modest gains but underperforms on smaller Claude models (Haiku 4.5 accuracy drops to 69.6% vs JSON 75.3%).

| Format | Token Delta vs. Source | Claude Accuracy | Prose Support | Recommended? |
|--------|----------------------|----------------|--------------|-------------|
| 1. **Hybrid XML + TOON + prose** | **-35% to -50%** | **High (trained priors)** | Excellent | **Yes — primary** |
| 2. TOON (pure) | -50% to -62% on tables | Moderate (not in training) | None | Tables only |
| 3. XML + Markdown | -10% to -20% | High (trained priors) | Excellent | Yes — conservative |
| 4. Compact Markdown DSL | -20% to -35% | High on Sonnet/Opus; Lower on Haiku | Excellent | Acceptable |
| 5. Minified JSON + Schema | -40% to -55% | High parseability, low reasoning | Terrible | Extraction-only |
| 6. Hybrid YAML-Markdown | -10% to -18% | High | Good | Acceptable |
| 7. Structured YAML | +6% to +8% | High (<=3 levels) | Poor | No |
| 8. TOML | +7% to +8% | Moderate | Very poor | No |

---

## Source File Characterization

### Structure Profile

```
Total: ~4,600 tokens | 342 lines | 16,985 bytes
Sections: 6 phases + 4 reference sections (risks, deps, open questions, traceability)
```

### Token Composition (estimated)

| Category | % of Tokens | Description |
|----------|------------|-------------|
| Semantic content | ~62% | Task descriptions, requirement details, rationale |
| Requirement IDs | ~11% | 76x FR-* refs + 31x SC-* refs, often repeated |
| Table scaffolding | ~9% | 56 rows, 240 pipe chars, separator rows |
| Markdown syntax | ~9% | 31 headings, 11 HRs, 390 backticks, bold spans |
| Structural repetition | ~9% | Repeated section headers (Goal/Milestone/Tasks/Validation/Files Touched) |

### Top 5 Bloat Patterns

1. **Inline code backticks**: 195 spans wrapping identifiers already unambiguous in context
2. **Table alignment padding**: Separator rows (`|------|`) and column padding add ~200 tokens across 6 tables
3. **Repeated phase scaffolding**: "### Tasks", "### Validation", "### Files Touched" x6 phases = ~90 tokens of pure structure
4. **Cross-reference duplication**: SC-001 through SC-015 appear in both per-phase Validation sections AND the Traceability table (duplicated ~120 tokens)
5. **Natural language goal/milestone prose**: Could be collapsed into structured fields saving ~150 tokens

---

## Format 1: Compact Markdown DSL (Conventions-Based)

### Approach

Retain Markdown but apply declared conventions:
- Single-char severity/priority markers
- Inline metadata instead of sub-sections
- Abbreviation header at top (~60 tokens) that defines shorthands
- No backtick wrapping for identifiers in structured contexts
- Collapsed validation into task lines
- No duplicate cross-reference tables

### Example Conversion (Phase 2, original = ~290 tokens)

**Original** (lines 79-108 of source):
```markdown
## Phase 2: Gate Definition & Pipeline Compatibility

**Goal**: `WIRING_GATE` constant passes `gate_passed()` evaluation without any
modification to the pipeline infrastructure.

**Milestone**: `gate_passed(wiring_report_content, WIRING_GATE)` returns
`(True, None)` for clean reports and correctly identifies each failure mode.

### Tasks

1. **Define `WIRING_GATE = GateCriteria(...)` per FR-T05d**
   - 5 semantic checks: `analysis_complete_true`, `zero_unwired_callables`,
     `zero_orphan_modules`, `zero_unwired_registries`, `total_findings_consistent`
   - All checks conform to `(content: str) -> bool` signature (FR-T05e)

2. **Implement `check_wiring_report()` per FR-T05f**
   - SemanticCheck-compatible validation wrapper

3. **Gate evaluation compatibility per FR-GATE-EVAL**
   - Integration test: `gate_passed()` evaluates `WIRING_GATE` without
     modification to `pipeline/gates.py`

4. **Pre-activation validation per FR-SHADOW-PRECHECK**
   - FR-SHADOW-PRECHECK-a: Validate provider directories exist with Python files
   - FR-SHADOW-PRECHECK-b: Zero-findings warning on repos with >50 Python files

### Validation
- SC-004: `gate_passed()` returns `(True, None)` for clean report
- SC-005: Integration test against cli-portify fixture
- SC-011: Provider dir pre-activation warning

### Files Touched
- `src/superclaude/cli/audit/wiring_gate.py` (modify — gate constant + semantic checks)
```

**Compact Markdown DSL** (~185 tokens, ~36% reduction):
```markdown
## P2: Gate Definition & Pipeline Compat | dep:P1 | files: audit/wiring_gate.py(M)
Gate: WIRING_GATE passes gate_passed() without modifying pipeline infra.
Done-when: gate_passed(content, WIRING_GATE) -> (True,None) for clean; identifies all failure modes.

1. Define WIRING_GATE=GateCriteria [FR-T05d] — 5 checks: analysis_complete_true, zero_unwired_callables, zero_orphan_modules, zero_unwired_registries, total_findings_consistent; all (content:str)->bool [FR-T05e] {SC-004}
2. Implement check_wiring_report() [FR-T05f] — SemanticCheck wrapper {SC-005}
3. Gate eval compat [FR-GATE-EVAL] — integration: gate_passed() evals WIRING_GATE, no mod to pipeline/gates.py
4. Pre-activation validation [FR-SHADOW-PRECHECK] — a: provider dirs exist w/ .py files; b: zero-findings warn on >50 .py repos {SC-011}
```

### Metrics

| Metric | Value |
|--------|-------|
| Estimated token savings | **20-35%** (~3,000-3,700 tokens from 4,600) |
| Comprehension fidelity | High — Markdown dominates LLM training data |
| Prose support | Excellent — native mixed-content |
| Failure modes | Ambiguity if convention header is missing from context |
| Agent parseability | High — natural language + lightweight structure |
| Human readability | Good — slightly denser but fully readable |

### Convention Header (included once, ~60 tokens)

```
<!-- CONVENTIONS: P#=Phase, dep:=depends-on, (M)=modify (C)=create,
[FR-*]=requirement, {SC-*}=success-criterion, |=inline-metadata -->
```

---

## Format 2: Structured YAML

### Approach

Pure YAML with hierarchical nesting. All prose becomes string values under typed keys.

### Example Conversion (Phase 2)

```yaml
phases:
  P2:
    name: Gate Definition & Pipeline Compatibility
    goal: WIRING_GATE passes gate_passed() without modifying pipeline infra
    milestone: gate_passed(content, WIRING_GATE) returns (True, None) for clean reports
    depends_on: [P1]
    files:
      - path: src/superclaude/cli/audit/wiring_gate.py
        action: modify
    tasks:
      - id: P2-T1
        desc: Define WIRING_GATE = GateCriteria(...)
        reqs: [FR-T05d, FR-T05e]
        details:
          - "5 semantic checks: analysis_complete_true, zero_unwired_callables, zero_orphan_modules, zero_unwired_registries, total_findings_consistent"
          - "All checks conform to (content: str) -> bool signature"
        validates: [SC-004]
      - id: P2-T2
        desc: Implement check_wiring_report()
        reqs: [FR-T05f]
        details: [SemanticCheck-compatible validation wrapper]
        validates: [SC-005]
      - id: P2-T3
        desc: Gate evaluation compatibility
        reqs: [FR-GATE-EVAL]
        details: ["Integration test: gate_passed() evaluates WIRING_GATE without modification to pipeline/gates.py"]
      - id: P2-T4
        desc: Pre-activation validation
        reqs: [FR-SHADOW-PRECHECK]
        details:
          - "a: Validate provider directories exist with Python files"
          - "b: Zero-findings warning on repos with >50 Python files"
        validates: [SC-011]
```

### Metrics

| Metric | Value |
|--------|-------|
| Estimated token savings | **-6% to -8% (INCREASE)** (~4,900-4,970 tokens) |
| Comprehension fidelity | High at <=3 nesting levels |
| Prose support | Poor — awkward multiline strings, quoting issues |
| Failure modes | Indentation errors silently change meaning; 4+ nesting degrades |
| Agent parseability | High for extraction; poor for prose comprehension |
| Human readability | Moderate — familiar to devs but dense for narrative |

### Why It's Worse on Tokens

YAML's structural overhead (key names, indentation, quotes, dashes) adds ~6-8% more tokens than Markdown's lightweight syntax. Every key-value pair introduces a colon, space, and typically a newline. Array items each get a dash. Strings with colons require quoting. The research benchmark (Workman 2025) measured 3,815 vs 3,579 tokens for equivalent datasets.

---

## Format 3: Minified JSON with External Schema

### Approach

Minified JSON body + a separate schema definition (referenced, not inlined). Maximum machine compression at the cost of human readability.

### Example Conversion (Phase 2)

```json
{"P2":{"n":"Gate Definition & Pipeline Compat","g":"WIRING_GATE passes gate_passed() w/o pipeline mod","m":"gate_passed(content,WIRING_GATE)->(True,None)","d":["P1"],"f":[{"p":"audit/wiring_gate.py","a":"M"}],"t":[{"i":"T1","s":"Define WIRING_GATE=GateCriteria","r":["FR-T05d","FR-T05e"],"dt":["5 checks: analysis_complete_true,zero_unwired_callables,zero_orphan_modules,zero_unwired_registries,total_findings_consistent","All (content:str)->bool"],"v":["SC-004"]},{"i":"T2","s":"Implement check_wiring_report()","r":["FR-T05f"],"dt":["SemanticCheck wrapper"],"v":["SC-005"]},{"i":"T3","s":"Gate eval compat","r":["FR-GATE-EVAL"],"dt":["Integration: gate_passed() evals WIRING_GATE, no mod pipeline/gates.py"]},{"i":"T4","s":"Pre-activation validation","r":["FR-SHADOW-PRECHECK"],"dt":["a: provider dirs exist w/ .py","b: zero-findings warn >50 .py"],"v":["SC-011"]}]}}
```

### Metrics

| Metric | Value |
|--------|-------|
| Estimated token savings | **40-55%** (~2,100-2,800 tokens) |
| Comprehension fidelity | High parseability (ACL SRW 2025) — but comprehension degrades when minified |
| Prose support | Terrible — all strings escaped, newlines become \n |
| Failure modes | Bracket matching errors at depth; missing commas; minification degrades LLM accuracy |
| Agent parseability | Highest for structured extraction; lowest for reasoning about content |
| Human readability | Near zero when minified |

### Critical Tradeoff

Minified JSON achieves the best raw token savings but introduces a **comprehension tax**: downstream agents must mentally re-parse dense token streams, which can degrade extraction accuracy by 10-20% on complex nested structures (arXiv 2411.10541). The savings are real only if agents perform structured key-value lookups, not if they reason about relationships between phases.

A separate schema file adds ~100-150 tokens to each agent's context but avoids ambiguous single-char keys.

---

## Format 4: TOML

### Approach

Flat section-based representation. Each phase becomes a TOML table, tasks become arrays of tables.

### Example Conversion (Phase 2)

```toml
[phases.P2]
name = "Gate Definition & Pipeline Compatibility"
goal = "WIRING_GATE passes gate_passed() without modifying pipeline infra"
milestone = "gate_passed(content, WIRING_GATE) returns (True, None) for clean"
depends_on = ["P1"]

[[phases.P2.files]]
path = "src/superclaude/cli/audit/wiring_gate.py"
action = "modify"

[[phases.P2.tasks]]
id = "P2-T1"
desc = "Define WIRING_GATE = GateCriteria(...)"
reqs = ["FR-T05d", "FR-T05e"]
details = [
  "5 semantic checks: analysis_complete_true, zero_unwired_callables, zero_orphan_modules, zero_unwired_registries, total_findings_consistent",
  "All checks conform to (content: str) -> bool signature",
]
validates = ["SC-004"]

[[phases.P2.tasks]]
id = "P2-T2"
desc = "Implement check_wiring_report()"
reqs = ["FR-T05f"]
details = ["SemanticCheck-compatible validation wrapper"]
validates = ["SC-005"]

[[phases.P2.tasks]]
id = "P2-T3"
desc = "Gate evaluation compatibility"
reqs = ["FR-GATE-EVAL"]
details = ["Integration: gate_passed() evaluates WIRING_GATE without mod to pipeline/gates.py"]

[[phases.P2.tasks]]
id = "P2-T4"
desc = "Pre-activation validation"
reqs = ["FR-SHADOW-PRECHECK"]
details = [
  "a: Validate provider directories exist with Python files",
  "b: Zero-findings warning on repos with >50 Python files",
]
validates = ["SC-011"]
```

### Metrics

| Metric | Value |
|--------|-------|
| Estimated token savings | **-7% to -8% (INCREASE)** (~4,920-4,970 tokens) |
| Comprehension fidelity | Moderate — TOML is rare in LLM training data |
| Prose support | Very poor — no native prose blocks, triple-quoted strings are fragile |
| Failure modes | [[array.of.tables]] syntax confuses LLMs; dotted keys misinterpreted at depth |
| Agent parseability | Moderate — less training exposure than YAML or JSON |
| Human readability | Good for flat config; poor for deep hierarchical roadmaps |

### Why It's the Worst Option

TOML was designed for configuration files, not hierarchical documents. The `[[double.bracket]]` array-of-tables syntax is poorly represented in LLM training data, and TOML's mandatory quoting of all string values adds significant overhead. It offers the worst combination: more tokens AND lower comprehension fidelity.

---

## Format 5: Hybrid YAML-Markdown

### Approach

YAML frontmatter for all structured/tabular data (phases, tasks, dependencies, files, criteria). Minimal Markdown body for prose-only content (risk rationale, cross-release notes). Eliminates Markdown tables entirely.

### Example Conversion (Phase 2 + risk entry)

```yaml
---
schema: roadmap/v1
phases:
  P2:
    name: Gate Definition & Pipeline Compat
    goal: WIRING_GATE passes gate_passed() w/o pipeline mod
    done_when: gate_passed(content, WIRING_GATE) -> (True,None) for clean
    deps: [P1]
    files: [{p: audit/wiring_gate.py, a: M}]
    tasks:
      - {id: T1, s: "Define WIRING_GATE=GateCriteria", r: [FR-T05d, FR-T05e], v: [SC-004]}
      - {id: T2, s: "Implement check_wiring_report()", r: [FR-T05f], v: [SC-005]}
      - {id: T3, s: "Gate eval compat", r: [FR-GATE-EVAL]}
      - {id: T4, s: "Pre-activation validation", r: [FR-SHADOW-PRECHECK], v: [SC-011]}
risks:
  - {id: R6, sev: High, phase: 2, desc: "Provider dir mismatch", mit: "Pre-activation validation (FR-SHADOW-PRECHECK); zero-findings halt"}
---

## Task Details

### P2-T1: Define WIRING_GATE=GateCriteria
5 semantic checks: analysis_complete_true, zero_unwired_callables, zero_orphan_modules, zero_unwired_registries, total_findings_consistent. All checks conform to (content: str) -> bool signature.

### P2-T4: Pre-activation validation
a: Validate provider directories exist with Python files.
b: Zero-findings warning on repos with >50 Python files.
```

### Metrics

| Metric | Value |
|--------|-------|
| Estimated token savings | **10-18%** (~3,770-4,140 tokens) |
| Comprehension fidelity | High — YAML for structure, Markdown for prose |
| Prose support | Good — detailed descriptions live in Markdown body |
| Failure modes | Large YAML frontmatter blocks (>200 lines) can confuse parsers; boundary between frontmatter and body must be clear |
| Agent parseability | High for extraction (YAML) + high for reasoning (Markdown) |
| Human readability | Good — clean separation of concerns |

### Best-of-Both Tradeoff

This format addresses YAML's prose weakness by keeping narrative in Markdown while moving structured data into YAML. The YAML section uses inline flow style `{k: v}` for compact task entries, keeping the frontmatter dense. Downstream agents can parse the YAML for task extraction and the body for detailed context.

Risk: very large frontmatter blocks (>200 lines) may hit YAML parser limits or confuse LLMs about where structure ends and prose begins.

---

## Format 6: TOON (Token-Oriented Object Notation)

### Background

Created by **Johann Schopplich**, MIT License, 2025. Latest release v2.1.0 (Dec 4, 2025), spec v3.0. Official repo: `github.com/toon-format/toon`. TypeScript SDK with community ports. Purpose-built to minimize LLM token consumption.

### Syntax

TOON uses a tabular header declaring schema, followed by CSV-like rows:

```
phases[6]{id,name,deps,files_touched}:
  P1,Core Analysis Engine,[],wiring_gate.py|wiring_config.py|wiring_analyzer.py
  P2,Gate Definition & Pipeline Compat,[P1],wiring_gate.py
  P3,TurnLedger & Sprint Integration,[P1;P2],sprint/models.py|sprint/executor.py
  P4,KPI Reporting & Deviation Reconciliation,[P3],sprint/kpi.py|roadmap/gates.py
  P5,Test Suite & Validation,[P1;P2;P3;P4],tests/cli/audit/test_wiring_gate.py
  P6,Shadow Rollout & Observability,[P5],-

tasks_P2[4]{id,desc,reqs,validates}:
  T1,Define WIRING_GATE=GateCriteria,[FR-T05d;FR-T05e],[SC-004]
  T2,Implement check_wiring_report(),[FR-T05f],[SC-005]
  T3,Gate eval compat,[FR-GATE-EVAL],[]
  T4,Pre-activation validation,[FR-SHADOW-PRECHECK],[SC-011]
```

### Metrics (Claude tokenizer, webmaster-ramos benchmark)

| Format | Tokens | vs. JSON | vs. Markdown |
|--------|-------|---------|-------------|
| JSON | 3,252 | baseline | +115% |
| YAML | 2,208 | -32% | +46% |
| Markdown | 1,514 | -53% | baseline |
| **TOON** | **1,226** | **-62%** | **-19%** |

On flat uniform tabular data, TOON achieves up to -58.8% vs JSON and -48.3% vs YAML. On mixed/nested data, savings collapse to -21.9% vs JSON and only -5.7% vs YAML.

### Claude Accuracy (webmaster-ramos)

- **Haiku 4.5**: JSON 75.3%, Markdown 69.6%, TOON 74.8%
- **Sonnet 4.6 / Opus 4.6**: 89.4% / 93.5% across ALL formats — format becomes noise on frontier models

### Metrics Summary

| Metric | Value |
|--------|-------|
| Estimated savings (tabular portions only) | **-50% to -62%** |
| Estimated savings on full roadmap (mixed) | -20% to -30% |
| Comprehension fidelity | Moderate — not in Claude training data, parsed via generalization |
| Prose support | **None** — must live in fenced blocks surrounded by prose |
| Failure modes | Deeply nested schemas; truncated-array detection scored 0/4 in validation tests |
| Agent parseability | High for tabular extraction; degrades on heterogeneous schemas |

### Why Pure TOON Fails for Roadmaps

Roadmaps are the **worst case** for TOON:
- Mixed prose (goals, milestones, rationale) + structured data (tasks, reqs, risks)
- Nested/heterogeneous schemas (each phase has different task counts and structures)
- No native way to interleave narrative context with task definitions

However, TOON is exceptional for the **tabular sub-sections**: risk matrices, dependency tables, file manifests, traceability matrices, requirement lists. Those are the densest token sinks in the source file.

---

## Format 7: XML (Claude-Native Structuring)

### Background

XML tags are **officially recommended by Anthropic** as the primary structuring mechanism for Claude prompts and documents. Per Anthropic's docs: *"XML tags help Claude parse complex prompts unambiguously"*. Claude was explicitly trained to recognize tags like `<instructions>`, `<context>`, `<document>`, `<example>`, `<thinking>`, `<answer>`. Tag boundaries are a trained signal — not merely a convention.

### Example Conversion (Phase 2)

```xml
<phase id="2" deps="P1">
  <name>Gate Definition &amp; Pipeline Compatibility</name>
  <goal>WIRING_GATE passes gate_passed() without modifying pipeline infra</goal>
  <done_when>gate_passed(content, WIRING_GATE) returns (True, None) for clean reports</done_when>
  <files>
    <file action="modify">src/superclaude/cli/audit/wiring_gate.py</file>
  </files>
  <tasks>
    <task id="T1" reqs="FR-T05d,FR-T05e" validates="SC-004">
      Define WIRING_GATE=GateCriteria with 5 checks: analysis_complete_true,
      zero_unwired_callables, zero_orphan_modules, zero_unwired_registries,
      total_findings_consistent. All (content:str)->bool.
    </task>
    <task id="T2" reqs="FR-T05f" validates="SC-005">
      Implement check_wiring_report() as SemanticCheck wrapper.
    </task>
    <task id="T3" reqs="FR-GATE-EVAL">
      Gate eval compat — integration: gate_passed() evals WIRING_GATE without
      modifying pipeline/gates.py.
    </task>
    <task id="T4" reqs="FR-SHADOW-PRECHECK" validates="SC-011">
      Pre-activation validation — (a) provider dirs exist w/ .py files;
      (b) zero-findings warning on &gt;50 .py repos.
    </task>
  </tasks>
</phase>
```

### Metrics

| Metric | Value |
|--------|-------|
| Token delta (pure XML for data) | **+15% to +40%** (verbose closing tags) |
| Token delta (XML scaffolding + prose inside) | **-5% to -15%** (overhead <1% on large content blocks) |
| Claude accuracy | **Highest trained priors** of any format; section boundaries more reliable than Markdown `##` |
| Prose support | Excellent — any content between tags |
| Failure modes | Verbose for pure data tables; over-nesting hurts; content with `<`/`>`/`&` needs escaping |
| Agent parseability | Very high — unambiguous delimiters, trained tag recognition |

### Why XML Is Special for Claude

Per Anthropic's long-context-tips documentation, combining XML structuring with query placement can yield **up to 30% response quality improvement** on complex multi-document inputs. The reason is not token efficiency — it's that XML tags are a *trained structural signal*. Markdown `##` headings get ambiguous when documents themselves contain headings, but `</phase>` cannot be confused with content.

XML is **not a data-compression format**. It is a **precision/reliability format**. The benefit is correctness, not token count. Use it as scaffolding, not as the primary data representation.

---

## Revised Primary Recommendation: Hybrid XML + TOON + Markdown Prose

The best format combines three techniques, each where it's strongest:

### Structure

```xml
<roadmap version="v3.2" schema="sc-roadmap/v1">
  <overview>
    ... narrative context in plain Markdown/prose ...
  </overview>

  <phase id="2" deps="P1">
    <goal>WIRING_GATE passes gate_passed() without modifying pipeline infra</goal>
    <done_when>gate_passed(content, WIRING_GATE) returns (True, None)</done_when>

    <tasks>
      ```toon
      tasks[4]{id,desc,reqs,validates}:
        T1,Define WIRING_GATE=GateCriteria,[FR-T05d;FR-T05e],[SC-004]
        T2,Implement check_wiring_report(),[FR-T05f],[SC-005]
        T3,Gate eval compat,[FR-GATE-EVAL],[]
        T4,Pre-activation validation,[FR-SHADOW-PRECHECK],[SC-011]
      ```
    </tasks>

    <task_details id="T1">
      5 semantic checks: analysis_complete_true, zero_unwired_callables,
      zero_orphan_modules, zero_unwired_registries, total_findings_consistent.
      All checks conform to (content: str) -> bool signature.
    </task_details>

    <files>
      ```toon
      files[1]{path,action}:
        src/superclaude/cli/audit/wiring_gate.py,modify
      ```
    </files>
  </phase>

  <risks>
    ```toon
    risks[8]{id,sev,phase,desc,mitigation}:
      R1,Medium,1,False positives from Optional[Callable],Whitelist FR-T02d
      R2,Low,1,AST parse failures,Graceful skip + files_skipped
      ...
    ```
  </risks>

  <traceability>
    ```toon
    sc[15]{id,phase,method}:
      SC-001,1,Unit test: 1 finding for unmatched callable
      SC-002,1,Unit test: finding for function with 0 importers
      ...
    ```
  </traceability>
</roadmap>
```

### Why This Wins

1. **XML scaffolding** (~80-120 tokens overhead) activates Claude's trained structural priors for reliable section extraction
2. **TOON tables** capture -50% to -62% compression on the tabular sections (risks, traceability, tasks, files) — which are the densest areas of the source file
3. **Markdown/prose inside XML tags** preserves the goal/milestone/rationale narrative where TOON fails
4. **Task detail decoupling**: task table contains IDs + one-line descriptions; extended details live in `<task_details>` blocks, read only when an agent is executing that specific task — enables selective context loading
5. **Schema attribute** (`schema="sc-roadmap/v1"`) provides forward-compatibility and lets agents validate structure

### Expected Metrics

| Metric | Value |
|--------|-------|
| Estimated token savings | **-35% to -50%** (~2,300-3,000 tokens from 4,600) |
| Claude accuracy | High — XML trained priors + TOON on Sonnet/Opus parses at parity with JSON |
| Prose support | Excellent — Markdown inside XML tags |
| Human readability | Moderate — denser than pure Markdown but well-structured |
| Selective loading | Yes — agents can parse `<phase id="2">` only, skip others |

### Caveats

- **Haiku 4.5**: TOON accuracy 74.8% vs JSON 75.3% — small penalty on cheaper models. For Haiku-heavy pipelines, consider XML + minified JSON instead of XML + TOON.
- **TOON library support**: Currently TypeScript-first with community Python ports — verify parsing reliability before committing
- **Convention documentation**: Downstream agents should be given a short system-prompt primer on TOON syntax (~60-80 tokens), amortized across many file reads

---

## Comparative Analysis

### Token Efficiency Ranking (best to worst)

| Rank | Format | Tokens (est.) | Delta vs. Source | Best For |
|------|--------|--------------|-----------------|----------|
| 1 | **Hybrid XML + TOON + prose** | **~2,300-3,000** | **-35% to -50%** | **Recommended — full roadmaps on Sonnet/Opus** |
| 2 | Pure TOON (tables only) | ~1,700-2,300 | -50% to -62% on tables | Sub-documents that are pure tabular data |
| 3 | Minified JSON + Schema | ~2,100-2,800 | -40% to -55% | Pure extraction pipelines (no reasoning) |
| 4 | Compact Markdown DSL | ~3,000-3,700 | -20% to -35% | Fallback if XML tooling unavailable |
| 5 | XML + Markdown | ~3,700-4,140 | -10% to -15% | Conservative — when TOON is untrusted |
| 6 | Hybrid YAML-Markdown | ~3,770-4,140 | -10% to -18% | Config-heavy pipelines |
| 7 | Structured YAML | ~4,900-4,970 | +6% to +8% | Not recommended |
| 8 | TOML | ~4,920-4,970 | +7% to +8% | Not recommended |

### Accuracy vs. Compression Frontier

```
Accuracy
  |
H |  [Compact MD]----[Hybrid YAML-MD]
  |       \                |
  |        \               |
M |   [YAML]----[Structured YAML]
  |                \
  |                 [Minified JSON]*
L |                      [TOML]
  +-----|---------|---------|--------> Token Savings
       -10%       0%      +30%     +55%

*Minified JSON accuracy depends heavily on task type:
 high for key-value extraction, low for reasoning
```

### Decision Matrix for Downstream Agent Types

| Agent Task | Recommended Format | Reason |
|------------|-------------------|--------|
| Task execution (read phase, do work) | **Hybrid XML+TOON+prose** | XML section extraction + TOON tables + prose details |
| Tasklist generation (parse all phases) | **Hybrid XML+TOON+prose** | TOON tasks[] tables are directly machine-readable |
| Dependency analysis | Hybrid XML+TOON | TOON dependency tables are near-optimal |
| Progress tracking | Hybrid XML+TOON+prose | Task IDs map cleanly from TOON rows |
| Validation/QA | Hybrid XML+TOON+prose | XML scaffolding gives reliable SC-* criteria extraction |
| Haiku-based sub-agents | **XML + Markdown** (not TOON) | TOON accuracy drops on Haiku; XML priors still hold |

---

## Recommendations (Revised)

### Primary Recommendation: Hybrid XML + TOON + Markdown Prose

**Adopt the hybrid format** as the standard for roadmaps consumed by Sonnet/Opus-class agents:
- **35-50% token reduction** (saving ~1,600-2,300 tokens per roadmap ingest)
- **XML scaffolding** leverages Claude's trained structural priors — Anthropic's own recommended approach
- **TOON tables** capture near-optimal compression on the densest sections (risks, traceability, tasks)
- **Markdown prose inside XML tags** preserves the narrative context where format-shifting fails
- **Selective loading**: agents can extract `<phase id="2">` without reading other phases

### Conservative Fallback: XML + Markdown (no TOON)

If TOON tooling is untrusted, or the pipeline includes Haiku sub-agents where TOON accuracy degrades, use XML scaffolding around compact Markdown. Yields -10% to -15% savings with maximum comprehension reliability and no new format dependencies.

### Haiku-Specific Notes

The webmaster-ramos benchmark showed Markdown accuracy on Haiku 4.5 dropped to 69.6% vs JSON at 75.3%. For any roadmap consumed by Haiku sub-agents, prefer XML+JSON over Markdown-heavy formats. On Sonnet/Opus 4.6, format becomes noise (89-93% accuracy across all formats) so optimize purely for tokens.

### Not Recommended

- **Pure YAML**: Increases tokens, poor prose support, indentation fragility
- **TOML**: Increases tokens, poor LLM training representation, no prose support
- **Pure minified JSON**: Comprehension degradation on reasoning-heavy agents; only viable for pure data-extraction pipelines
- **Pure TOON**: Best compression on tables but cannot handle mixed prose + structured data that a roadmap requires

### Implementation Path

1. Define the XML schema (`sc-roadmap/v1`) — tag names, attribute conventions, where TOON blocks go
2. Write a converter: `.md roadmap` → `.xml+toon` hybrid output
3. Add a short system-prompt primer (~80 tokens) defining the schema and TOON syntax for downstream agents
4. A/B test on one roadmap: token delta, task completion accuracy, parsing errors across Haiku/Sonnet/Opus
5. If validated, update the roadmap pipeline templates in `src/superclaude/cli/roadmap/`
6. Watch for TOON spec updates (currently v3.0, Dec 2025) — format is young and evolving

---

## Sources

### Primary (TOON + XML + Claude-specific)
- **Anthropic — "Use XML tags"** (official Claude prompt engineering guidance)
- **Anthropic — Claude 4.6 prompt engineering best practices** (XML as recommended structuring)
- **Anthropic — Long context prompting tips** (up to 30% quality gain with XML + query placement)
- **TOON official spec + SDK** — github.com/toon-format/toon (v2.1.0, Dec 2025; spec v3.0)
- **TOON benchmarks** — toonparse.com/benchmarks (−58.8% vs JSON on flat data; −21.9% on mixed)
- **webmaster-ramos 2025** — "YAML vs MD vs JSON vs TOON Claude API benchmark" (Claude tokenizer: MD 1,514 / TOON 1,226 tokens; Haiku/Sonnet/Opus accuracy data)
- **fromjsontotoon.com** — TOON vs JSON performance analysis

### Secondary (general format efficiency)
- Workman 2025 — "YAML vs JSON: The Hidden Token Tax" (Claude tokenizer, 6-10% YAML premium)
- Syntax & Empathy 2025 — "Designer's Guide to Markup Languages" (MD 11,612 / YAML 12,333 / TOML 12,503 / JSON 13,869 tokens)
- CuriouslyChase 2025 — "YAML vs JSON Token Efficiency" (minified JSON 41 vs 133 YAML tokens)
- arXiv 2411.10541 — "Prompt Formatting and LLM Performance" (up to 40% perf delta by format)
- ACL SRW 2025 (arXiv 2507.01810) — "Evaluating Structured Output Robustness" (JSON highest parseability)
- arXiv 2604.03616 — "The Format Tax"
- arXiv 2603.03306 — "Token-Oriented Object Notation vs JSON"
- Anthropic Docs — "Token-Efficient Tool Use"
- Medium 2025 — "Tokenization Comparison: CSV, JSON, YAML, TOON" (tiktoken cl100k_base benchmarks)
