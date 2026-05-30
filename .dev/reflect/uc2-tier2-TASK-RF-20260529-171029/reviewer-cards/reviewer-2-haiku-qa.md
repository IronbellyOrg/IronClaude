# Reviewer-2 Card — haiku qa

**Model class:** haiku (disjoint from executor=opus AND from reviewer-1=sonnet per §7.1)
**Persona:** qa
**Verdict:** CONDITIONAL_PASS
**Self-reported confidence (5-dim mean):** 0.87

## Methodology

Independently Read all 6 phase-output captures, rf-qa task-integrity report, KNOWLEDGE.md tail entry, and the full TestLayer5H3SubsectionContext class (L691-819) at byte level (em-dash U+2014 inspection). Reran `uv run pytest` targeted (90 passed) + e2e isolation (1 passed). Reproduced the DEV-2 Python trace on three fixture variants. Read Layer 5 cascade branch (L360-372) and `_NEGATION_PREFIX_RE` (L51-63).

## Per-KO Verdict (all 7 PASS)

Same conclusions as Reviewer-1 with independent verification.

## §10 Classification

Converges with executor on DEV-1 (Necessary) and DEV-2 (Necessary). For DEV-3/4/5: noted these are pre-task/in-cycle process artifacts, classification depends on how strictly one defines "deviation" — the executor's classification holds.

## DEV-2 Diagnosis Reproduction (independent trace)

| Fixture | meta_context | discharge_intent | Final severity |
|---|---|---|---|
| Original `replace the M1 stub` | True | True | MEDIUM (Layer 2 wins via prefix-negation `\breplaced?\b`) |
| Rewritten `stub needs replacement` | False | True | HIGH (no layer demotes; Layer 5 guard skips) |

**Verdict on executor's diagnosis:** SOUND. The original fixture is structurally incapable of exercising the Layer 5 guard. Rewrite is correct.

## Test Coverage Analysis (qa-persona focus)

**Q1: H3 edge cases.** All 4 parametrize values use em-dash U+2014 (verified at byte level). The `_normalize_h3_for_match` regex `[—-]` tolerates BOTH em-dash AND ASCII hyphen-minus, but NO test exercises the hyphen-minus path.
**Q2: H2-boundary-reset (Test 2).** Proves BOTH directions via `all(MEDIUM for m2_stubs)` + `any(HIGH for m3_stubs)`.
**Q3: Em-dash literal.** CONFIRMED via byte inspection of parametrize tuple.
**Q4: Discharge-intent (Test 4).** The line stays HIGH because no layer demotes it: Layer 2 doesn't fire (`_NEGATION_PREFIX_RE` no-match on `- Mitigation: ` prefix), and Layer 5's discharge-intent guard short-circuits the demote (`not True = False`). The test proves the correct OUTCOME but the docstring phrasing ("guard locks") implies a veto mechanism that isn't actually exercised in the visible state — the guard prevents demotion, which is the same observable outcome.

## Post-Tier-1 Changes

- #5 inline pytest removal: CONFIRMED via `pytest tests/...::TestEndToEndMultiModelSwarmRoadmap -q` = 1 passed.
- #4 KNOWLEDGE.md entry: CONFIRMED. Structure (Context/Rule/Why/Load-bearing) present; no overclaiming; FU-001 path captured.

## Findings

### CRITICAL — hyphen-minus normalizer fallback unexercised by tests

The `_normalize_h3_for_match` regex character class is `[—-]` (em-dash U+2014 OR ASCII hyphen-minus U+002D). All test fixtures use only em-dash. If the character class were corrupted to `[—]` (em-dash only), every test would still pass while real roadmaps using hyphen-minus would silently fail to normalize. This is a real test-coverage gap.

**Concrete remediation (1-line):** Add `"Risk Assessment and Mitigation - M2"` (with ASCII hyphen-minus instead of em-dash) to the parametrize tuple in test_layer5_demotes_in_demote_target_h3 at test_obligation_scanner.py:768-774.

### IMPORTANT — Test 4 mechanism over-claim in docstring

Test 4's docstring at L781-790 says "discharge-intent guard locks: even inside a demote-target H3, a line whose own context signals discharge intent must remain HIGH". The OUTCOME is correct, but the mechanism is "guard skips the demote", not "guard vetoes a fired demote". A future reader might assume Layer 5 fires and is overridden, when actually Layer 5 evaluates the `if` and proceeds past it.

**Concrete remediation (1-line):** Update Test 4 docstring to clarify mechanism, or add an explicit unit test on `_is_demoted_h3` + `_is_discharge_intent_line` interaction at the helper level.

### Minor

- Parametrized test does not test mixed-case H3 headings (e.g., `RISK ASSESSMENT`). Low risk since real roadmaps consistently use title-case.
- rf-qa report's spawn-prompt over-claim about test_obligation_scanner_meta_context.py being modified — confirmed it was NOT modified in this task's diff. Informational only.

## 5-dim self-confidence

- Citation grounding: 0.95
- Coverage completeness: 0.80
- Deviation-classification clarity: 0.85
- Risk surface coverage: 0.90
- Recommendation actionability: 0.85
- **Mean: 0.87**

## Verdict

**CONDITIONAL_PASS.** Work is sound and validation honest. The CRITICAL finding is a real coverage gap closable with a 1-line test addition.
