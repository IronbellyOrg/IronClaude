# Tech-Research Prompt: CLI TDD Integration

**Use with:** `/tech-research`
**Scope:** `src/superclaude/cli/roadmap/`, `src/superclaude/cli/tasklist/`, `src/superclaude/cli/pipeline/`
**Output type:** Implementation plan — specific files, functions, and changes needed

---

## GOAL

The IronClaude CLI pipeline (`superclaude roadmap run <file>`, `superclaude roadmap validate`, `superclaude sprint run`) currently treats its input as a **specification file** (`release-spec-template.md` format) throughout every step. We want to be able to pass a **TDD file** (`src/superclaude/examples/tdd_template.md` format, 28 sections, 27 frontmatter fields) as the input instead, and have the roadmap pipeline extract richer structured content from TDD-specific sections to produce a higher-fidelity roadmap and tasklist.

Research every CLI file that touches the input document — prompts, gates, executors, parsers, scanners, validators — and produce a precise implementation plan for what must change.

---

## WHY

A prior research investigation (`RESEARCH-REPORT-prd-tdd-spec-pipeline.md`) thoroughly audited the **inference/skill layer** (`sc:roadmap` skill, `sc:tasklist` skill, `sc:spec-panel` command, `prd/tdd` skills) and found:

- sc:roadmap's extraction pipeline misses TDD §7 (Data Models), §8 (API Specs), §10 (Component Inventory), §14 (Observability), §15 (Testing Strategy), §19 (Migration), §25 (Operational Readiness) because it only captures behavioral "shall/must" statements
- sc:tasklist's `--spec` flag is declared in argument-hint but has zero body implementation
- The spec frontmatter fields (`spec_type`, `complexity_score`, etc.) are ignored by all pipeline logic
- Domain dictionaries have no Testing or DevOps/Ops domain, systematically miscounting TDD complexity

**That research was unaware of the programmatic CLI layer.** The actual execution path is:

```
superclaude roadmap run <spec_file>   ← Python CLI, NOT inference
    → cli/roadmap/executor.py           builds steps, embeds files into prompts
    → cli/roadmap/prompts.py            constructs prompt strings passed to Claude subprocess
    → cli/pipeline/process.py           spawns `claude --print -p "<prompt>"` subprocess
    → cli/pipeline/gates.py             validates Claude output via Python YAML/regex (NO inference)
    → cli/roadmap/gates.py              14 GateCriteria definitions (EXTRACT_GATE, GENERATE_A_GATE, etc.)
    → cli/roadmap/validate_executor.py  runs spec-fidelity check: roadmap vs original spec
    → cli/tasklist/executor.py          runs tasklist-fidelity check: roadmap vs tasklist
```

The implementation plan from the prior research needs to be re-evaluated and extended with this CLI layer in mind. The CLI layer is where the real integration work lives.

---

## WHERE TO LOOK

Investigate every file in these directories. Read source, not just filenames.

### Primary targets (must read every file)

| Directory | Files to read | Why |
|-----------|--------------|-----|
| `src/superclaude/cli/roadmap/` | `executor.py`, `commands.py`, `prompts.py`, `gates.py`, `models.py`, `spec_parser.py`, `validate_executor.py`, `validate_prompts.py`, `validate_gates.py`, `fidelity_checker.py`, `obligation_scanner.py`, `integration_contracts.py`, `convergence.py`, `semantic_layer.py` | This is the roadmap pipeline — every file touches the input document or validates against it |
| `src/superclaude/cli/tasklist/` | `executor.py`, `commands.py`, `prompts.py`, `gates.py`, `models.py` | Tasklist validation pipeline; the `--spec` flag gap identified in prior research may have CLI-level implications |
| `src/superclaude/cli/pipeline/` | `executor.py`, `process.py`, `gates.py`, `models.py`, `deliverables.py` | Generic step sequencer — understand how input embedding, gate checking, and parallel execution work |

### Secondary targets (read selectively)

| File | What to check |
|------|--------------|
| `src/superclaude/examples/tdd_template.md` | Full TDD structure: 28 sections, 27 frontmatter fields — this is the target input format |
| `.dev/releases/current/tdd-spec-analysis/RESEARCH-REPORT-prd-tdd-spec-pipeline.md` (exists) | Prior research findings — use as context, do NOT re-verify; treat as authoritative for the skills/commands layer |

---

## SPECIFIC QUESTIONS TO ANSWER

For each question, cite the actual file and line where evidence was found. Do not infer.

### Q1: Entry point — how does the spec file become a prompt?

- `commands.py`: What CLI flag receives the spec file? Is there any `--input-type` or format detection flag? What parameters are passed to the executor?
- `executor.py`: Trace exactly how the spec file path flows into the first pipeline step. When is `_embed_inputs()` called with the spec file? Which steps receive the spec file as an input vs. which steps only see the extraction output?
- `prompts.py:build_extract_prompt()`: Is the prompt hardcoded to assume "specification" language? Does it reference spec-specific sections or field names?

### Q2: The extract step — what would break for TDD input?

- The EXTRACT_GATE requires 13 YAML frontmatter fields (`spec_source`, `functional_requirements`, `complexity_class`, `domains_detected`, etc.). Would Claude produce these correctly when given a TDD whose sections use TypeScript interfaces, endpoint tables, and state machine diagrams instead of "shall/must" behavioral statements?
- The extract prompt instructs 8 specific body sections (Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions). Which of these would be sparsely populated from TDD input with the current prompt language?
- `domains_detected` field: the generate step reads this to know which domains to address. If a TDD has §15 Testing Strategy and §25 Operational Readiness, which are outside the 5 current domains (Frontend, Backend, Security, Performance, Documentation), how would those sections affect the generated roadmap?

### Q3: The generate step — what reads the extraction output?

- `prompts.py:build_generate_prompt()`: Read the full function. What extraction fields does the generate prompt reference? Are there any TDD-specific sections (component inventory, migration phases, test cases) that would be lost because they weren't captured in the extraction?
- Does the generate step receive the original spec/TDD file as input, or only the extraction output? If only extraction, then extraction coverage is the single chokepoint for TDD richness.

### Q4: The validate pipeline — what compares against the original spec?

- `validate_executor.py`, `validate_prompts.py`, `validate_gates.py`: What does the roadmap validate step do? Does it compare the generated roadmap against the original spec file? If so, what YAML fields does it require in its output (SPEC_FIDELITY_GATE)?
- `fidelity_checker.py`: What does this file do? Is it a programmatic checker or does it spawn a Claude subprocess? What inputs does it read?
- `obligation_scanner.py`: What obligations is it scanning for? Does it read the original spec file or the roadmap?
- `integration_contracts.py`: What integration contracts are being tracked? Does this have any dependency on spec-format-specific fields?
- `convergence.py`: What does convergence measure? What are its inputs?
- `semantic_layer.py`: What semantic layer is this? Does it parse the spec file in any way?

### Q5: The tasklist validate pipeline — what changes for TDD?

- `tasklist/executor.py`: The prior research confirmed the tasklist prompt explicitly says "validate ROADMAP → TASKLIST alignment ONLY. Do NOT compare the tasklist against the original specification." Is this boundary enforced purely in the prompt, or does Python also enforce it?
- `tasklist/prompts.py:build_tasklist_fidelity_prompt()`: Read the full function. Does it receive the spec/TDD file at all, or only the roadmap and tasklist?
- If we want tasklist tasks to be enriched from TDD §15 (Testing Strategy) for Validation fields, and TDD §19 (Migration) for Rollback fields, does this happen at the tasklist generation step (inference/skill layer) or at the tasklist validation step (CLI layer)?

### Q6: Gate constraints — what must TDD output satisfy?

- For each gate in `roadmap/gates.py` (EXTRACT_GATE, GENERATE_A/B_GATE, DIFF_GATE, DEBATE_GATE, SCORE_GATE, MERGE_GATE, ANTI_INSTINCT_GATE, TEST_STRATEGY_GATE, SPEC_FIDELITY_GATE, CERTIFY_GATE), identify:
  - Which YAML frontmatter fields are required
  - Which semantic checks run on the output
  - Whether any check is spec-specific (would fail or produce wrong results with TDD input)
- Specifically: `ANTI_INSTINCT_GATE` checks `fingerprint_coverage >= 0.7` — fingerprint of what? The spec? Would a TDD produce a different fingerprint?
- `SPEC_FIDELITY_GATE` checks `high_severity_count == 0` and `tasklist_ready == true` — fidelity of roadmap to what? The original spec or TDD?

### Q7: Auto-detection vs. explicit flag

- Does any existing file (executor, commands, parser) contain logic to detect whether the input is a spec vs. TDD format?
- `spec_parser.py`: What does this parse? Is it spec-specific or generic markdown?
- What would be the cleanest extension point: a new `--input-type [spec|tdd]` flag in `commands.py`, auto-detection based on YAML frontmatter `type` field in the executor, or a wrapper function in `prompts.py` that selects the appropriate extraction instructions?

### Q8: What existing extension points can be reused?

- The prior research found the `--spec` flag is declared in sc:tasklist's argument-hint but completely unimplemented in the skill body. Does a corresponding `--spec` flag or equivalent exist anywhere in the CLI layer (`tasklist/commands.py`)?
- Are there any TODO comments, feature flags, or `NotImplemented` placeholders in any roadmap or tasklist CLI file that suggest TDD support was anticipated?
- The `build_extract_prompt()` function has a `retrospective_content` optional parameter already — is there a similar pattern that could be used for TDD-specific context injection without a full prompt rewrite?

---

## OUTPUT NEEDED

A precise implementation plan with:

1. **For each file that must change**: the current behavior, the required change, the exact function/method/section to modify, and whether the change is additive (new code path) or modifies existing behavior.

2. **Gate compatibility analysis**: a table of all 14 gates showing whether each gate passes, fails, or needs modification when given TDD-derived Claude output.

3. **Data flow diagram**: ASCII or table showing exactly which pipeline steps receive the TDD/spec file as direct input vs. only see downstream artifacts (extraction, roadmap, etc.). This determines where TDD-awareness must be injected.

4. **Sequenced implementation order**: in what order should the changes be made to minimize risk and allow incremental testing? Which changes are prerequisites for others?

5. **Backward compatibility confirmation**: for each proposed change, confirm whether existing spec-format inputs continue to work unchanged.

---

## CONSTRAINTS

- All changes must be **backward compatible** — `superclaude roadmap run spec.md` must continue to work identically.
- The existing 14-step pipeline structure (extract→generate→diff→debate→score→merge→...) must remain intact; TDD support is additive.
- Do not propose changes to files outside `src/superclaude/cli/` — the skills/commands layer changes (sc:roadmap extraction improvements, sc:tasklist `--spec` implementation, TDD template frontmatter additions) are covered by the prior research report and are a separate work stream.
- Gate semantic checks in `gates.py` are pure Python with no subprocess calls — any gate changes must remain pure Python.

---

## KNOWN FACTS (do not re-verify, use as starting context)

From direct source reading prior to this research request:

- `cli/pipeline/process.py:ClaudeProcess.build_command()` spawns: `claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns <N> --output-format <text|stream-json> -p "<prompt>"`
- `cli/roadmap/executor.py:_embed_inputs()` reads files and wraps them as fenced code blocks inline in the prompt: `f"# {p}\n```\n{content}\n```"`
- `cli/roadmap/commands.py` takes `spec_file` as a positional argument (`click.argument("spec_file", ...)`) with `--output`, `--agents`, `--depth`, `--resume`, `--dry-run`, `--model`, `--max-turns` options — NO `--input-type` flag exists
- `cli/roadmap/prompts.py:build_extract_prompt()` hardcodes "Read the provided specification file" and instructs 13 specific YAML frontmatter fields + 8 body sections
- `cli/tasklist/prompts.py:build_tasklist_fidelity_prompt()` explicitly says "VALIDATION LAYERING GUARD: validate ROADMAP → TASKLIST ONLY. Do NOT compare the tasklist against the original specification."
- `cli/roadmap/gates.py` defines 14 GateCriteria including ANTI_INSTINCT_GATE (requires `fingerprint_coverage >= 0.7`) and SPEC_FIDELITY_GATE (requires `high_severity_count == 0`)
- The roadmap pipeline's generate step (`build_generate_prompt()`) reads the **extraction output**, not the original spec file directly — making the extract step the sole chokepoint for TDD section coverage
