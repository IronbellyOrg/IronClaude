# TFEP Run 2 — Minimal Corrective Solution Verdict

## Goal
Clear the two remaining failures while preserving STRICT scanner semantics and avoiding broad behavioral drift.

## Minimal corrective plan

### 1) Remove or narrowly gate discharge-intent hard skip
- Current behavior drops obligations on lines containing verbs like `remove/replace/...` before severity/meta-context classification.
- This suppresses valid MEDIUM meta-context obligations (inline code case).
- Minimal correction:
  - Do **not** unconditionally `continue` on `_is_discharge_intent_line`.
  - Let existing Layer-1/Layer-2 logic demote to `MEDIUM` when appropriate.

Why minimal: this restores expected non-empty obligation capture without expanding term vocabulary.

### 2) Keep FR-MOD1.1 word-boundary vocabulary strict
- Do not broaden regex to substring-in-identifier matching.
- `mock_data` is currently out-of-scope by design (`\bmock\b` semantics).

Why minimal: avoids broad detection drift and surprise new obligations across roadmap corpus.

### 3) Correct the failing code-block fixture to an in-vocabulary term
- Replace fixture token with an explicit scaffold term already covered by FR-MOD1.1 (for example `mock`/`mocked`/`stub`).
- Retain test intent: fenced-code obligations should be MEDIUM.

Why minimal: test now validates intended behavior (code-block severity demotion) rather than vocabulary expansion.

## Non-recommended option (drift-prone)
- Expanding scaffold regex to detect fragments inside identifiers (e.g., `mock_data`, `stub_client`) is broader than this incident requires and likely increases false positives.

## Acceptance criteria
- `test_inline_code_scaffold_term_is_medium` passes with non-empty MEDIUM obligations.
- `test_code_block_still_medium` passes using vocabulary-compliant fixture text.
- No unexpected increase in HIGH obligation counts on baseline roadmap tests.

## Escalation recommendation
- **standard** (mixed implementation + test correction, low blast radius if kept narrow).
