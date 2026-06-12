# Unmask and Sweep (H3)

H3 tests gates and parsers against **full generated artifacts** (containing executable positives AND sibling negatives), not snippets, and after any escape fix it searches for adjacent masked defects in the same family before closure. It closes **E2** (a substring classifier accepting `complete` inside `incomplete` and applying the wrong phase invariant) and **E3** (a single reported heading fixed while same-token sibling headings remained unswept). The H3 status feeds the §5.4 aggregation in [`hardening-output-contract.md`](hardening-output-contract.md).

## H3 parser decision — small formal allow-list grammar (§5.7)

H3 uses a **small formal allow-list grammar** for this increment — **not** ad hoc substring matching and **not** a full CommonMark parser. The grammar is intentionally narrow:

1. Only ATX headings (`#`, `##`, … with a required post-marker space) and explicit verdict/status lines are behavior-controlling.
2. Matching is exact-token or word-boundary anchored with escaped tokens (`\b` / `re.escape` / exact grammar); substring containment is **never** behavior-controlling.
3. Setext-like headings, decorated/bolded verdict lines, wrong-case tokens, and sibling sections are **fixtures**, not accepted control syntax unless explicitly added to the grammar later.
4. Every grammar expansion requires a positive fixture, a near-miss negative fixture, **and** a full-artifact mixed fixture.

## Word-boundary rule + near-miss negatives (FR-8)

Phase / verdict / completion-signal / resume-token matching uses **word-boundary-anchored matching** (`\b` / `re.escape` / exact grammar). This is a **first-class blocking rule**, not an appendix note (fixes adversarial F-SC1). It closes the E2 substring collision directly.

Mandatory near-miss negative fixtures (regex timeouts are a guardrail, **not** a substitute for these):

- `incomplete` (must not match `complete`)
- `representation` (must not match `present`)
- decorated / bolded verdict lines
- wrong-case tokens
- setext-like headings

## Whole-artifact classifier required controls (FR-7)

A passing H3 requires all of:

- a **positive case** — the intended violation is still caught;
- a **sibling / off-path negative** — a same-token/same-shape non-target does NOT hard-fail;
- a **full-artifact case** containing both positive and sibling-negative controls together;
- a **severity assertion** (`HALT` / `WARN` / `CONTINUE`) per runtime consumer.

## Unmask-and-sweep regression (FR-9)

H3 **FAILs** if a fix only addresses the reported repro without searching same-token/same-shape sibling surfaces, **or** if a heuristic parser over generated prose is hard-fatal without adversarial false-positive fixtures plus a cost rationale. The sweep documents `K_true` and `K_swept` and asserts `K_swept` covers the full sibling family.

## H3 Unmask / Sweep / Classifier Card schema (§5.6)

| Field | Required | Meaning |
|-------|----------|---------|
| `anchor_failure` | yes | The original failure or repro that motivated the fix |
| `sibling_family_discovery_method` | yes | How same-token/same-shape sibling surfaces were discovered |
| `K_true` | yes | Count/list of sibling-family members discovered |
| `K_swept` | yes | Count/list of sibling-family members covered by fixtures or proof |
| `coverage_proof` | yes | Evidence that `K_swept` covers the full sibling family |
| `positive_fixture` | yes | Full-artifact or fixture case where the intended violation still HALTs |
| `sibling_negative_fixture` | yes | Same-token/same-shape off-path case that must not hard-fail |
| `full_artifact_mixed_fixture` | yes | Generated artifact containing positive and sibling-negative controls together |
| `severity_assertions_by_consumer` | yes | Expected HALT/WARN/CONTINUE for every runtime consumer |
| `heuristic_cost_rationale` | required for hard-fatal heuristic parser | Why the heuristic is worth hard-gating despite false-positive risk |
