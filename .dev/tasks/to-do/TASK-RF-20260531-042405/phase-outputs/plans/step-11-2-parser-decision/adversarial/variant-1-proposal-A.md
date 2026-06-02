# Variant 1 — Proposal A: Relocate ONE canonical parser into the envelope module

## Problem being solved
24 in-gate semantic checks in `roadmap/gates.py` call the local `_parse_frontmatter(content)`. Step 11.2(d) says consumers should read `envelope.frontmatter` "via dependency injection … not by re-parsing the markdown artifact," but the gate dispatch passes only `content: str` (`pipeline/gates.py:84`, `check.check_fn(content)`), and the envelope never reaches semantic checks.

## Mechanism
1. **Add `extract_frontmatter(content: str) -> dict` to `cli/roadmap/envelope.py`** — the single canonical frontmatter parser, owned by the post-step-extractor module (per §MVR §1 "one `_parse_frontmatter` lives in the post-step extractor only").
2. **Add a typed `frontmatter: dict` field to `PipelineEnvelope`**, populated by the post-step extractor (which calls `extract_frontmatter` on the step artifact).
3. **The 24 in-gate semantic checks import `extract_frontmatter` from the envelope module** and call it on the `content: str` they already receive. The `SemanticCheck.check_fn: Callable[[str], bool|str]` signature and the `gate_passed` dispatch are UNCHANGED.
4. **Delete the 5 other variants**: `roadmap/gates.py:_parse_frontmatter` L178 (replaced by import), `pipeline/gates.py:_check_frontmatter` L125, `spec_parser.py:parse_frontmatter` L114, `spec_patch.py:_extract_frontmatter` L285. Cross-cutting `cli_portify/utils.py:11` + `audit/wiring_gate.py:931` import the canonical parser or are flagged for parser-consistency lint.
5. **Cross-step consumers** (those that need parsed state from a PRIOR step) read `envelope.frontmatter` (true dependency injection). **In-gate local validators** (the 24, validating the file they are gating) call the canonical parser on their own `content`.
6. **Any check that genuinely needs cross-step state becomes a `CodeAssertion`** (the R1.3 envelope-aware tier), NOT a `SemanticCheck`.

## How it satisfies the contracts
- **Contract #6 (parser consistency):** exactly ONE parser exists → divergence is structurally impossible (the split-personality bug is eliminated).
- **§MVR §1 (substrate inversion):** cross-step STATE flows through the typed envelope; the two divergent parsers are deleted; the one parser lives in the envelope module.
- **Flaw 3 (state-in-markdown):** addressed — cross-step state is the envelope's job. A gate validating its OWN output file's frontmatter is local validation, not cross-step state transport.
- **Tier separation (R1.3):** `SemanticCheck` stays content-local; `CodeAssertion` stays envelope-aware. The two tiers the rewrite deliberately created remain distinct.

## Reinterpretation of 11.2(d) (must be documented)
The literal phrase "not by re-parsing the markdown artifact" is met for cross-step consumers (DI) but NOT for in-gate local validators, which call the canonical parser on the file under inspection. This is a NECESSARY deviation justified by two grounded facts: (i) `gate_passed` in the generic `execute_pipeline` passes no envelope (`pipeline/executor.py:267`); (ii) the post-step extractor populates `envelope.frontmatter` AFTER the step runs (`executor.py:1491`), so the current step's frontmatter does not exist in the envelope at gate time.

## Blast radius
- Files touched: `envelope.py` (+1 function, +1 field), `roadmap/gates.py` (swap 24 callsites to the imported parser + delete local def), delete 3 other defs, 2 cross-cutting imports, new `test_parser_consistency.py`.
- Dispatch substrate: UNCHANGED. `pipeline/models.py` UNCHANGED. `pipeline/executor.py` UNCHANGED. Sprint pipeline: UNTOUCHED. Other 7 SemanticCheck-consuming modules: UNTOUCHED.

## Risks
- Must confirm the relocated parser is byte-behaviour-equivalent to the canonical-chosen variant (the consistency test covers this).
- If a specific one of the 24 checks turns out to need cross-step frontmatter, it must be promoted to a CodeAssertion (caveat, not a blocker).
