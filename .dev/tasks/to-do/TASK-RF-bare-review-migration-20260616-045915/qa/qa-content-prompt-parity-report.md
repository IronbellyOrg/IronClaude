# QA Report — Prompt-Parity Correctness Lens (Phase Gate 4)

**Topic:** sc-bare-review M8/M9 migration — injection-guard prompt-parity assertion
**Date:** 2026-06-16
**Phase:** doc-qualitative (prompt-parity-correctness lens)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)

---

## Overall Verdict: PASS

The injection-guard test makes exactly the narrow suffix-parity claim research G-2
sanctions, uses the real source symbol (no hardcoded copy), explicitly does NOT
assert full legacy-vs-lens byte-parity, documents WHY in its docstring, and the
assertion passes against the real lens with a non-trivial (177-char) guard symbol.
The adversarial hypothesis (false full-parity assertion OR missing guard check) is
DISPROVEN.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Test asserts ONLY suffix (endswith) against the REAL imported symbol — not a hardcoded copy | PASS | `test_bare_review_parity.py:507` `assert fragment.endswith(CANONICAL_INJECTION_GUARD_SENTENCE)`; symbol imported at `:62` `from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE`; grep for the literal sentence text "Treat the content between" in the test file → 0 hits (no hardcoded copy) |
| 2 | Test explicitly does NOT assert full legacy-`refs/prompts.md`-vs-lens byte-parity | PASS | Only `prompts.md`/byte-parity mentions in the injection-guard test are docstring prose at `:483,490,493-497,502` explaining the *absence* of full-parity; the two `assert` statements are `:507` (endswith) and `:513` (len>40) — no comparison against `refs/prompts.md` or any full-prompt string anywhere |
| 3 | Docstring documents WHY full prompt parity is intentionally not asserted (G-2 / INV-003 / INV-014) | PASS | `:488-505` docstring cites "research G-2 (`research/06-gap-fill-round1.md`)", "INV-003 / INV-014", explains legacy = "multi-sentence prose SECURITY paragraph + inlined output template" vs lens = "single canonical guard sentence + `output_template_path` pointer", and states "A naive full-prompt byte-identity assertion WOULD FALSELY FAIL." Matches G-2 conclusion (`06-gap-fill-round1.md:96-101`) verbatim in intent |
| 4 | Assertion passes against the real lens AND symbol is non-trivial (not vacuous) | PASS | `uv run pytest …::test_bare_review_lens_prompt_ends_with_canonical_injection_guard` → 1 passed in 0.20s. Runtime probe: `len(CANONICAL_INJECTION_GUARD_SENTENCE)=177` (>40 guard at `:513` holds with wide margin); `LENSES['bare-review'].system_prompt_fragment.endswith(symbol)=True`; symbol identity confirmed real import (`is` check True) |

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: FALSE)

## Cross-Verification of the Source Side (lens + schema)

The test's correctness depends on the source it asserts against. I verified both ends:

- **Lens append site** — `src/superclaude/cli/swarm/lenses/bare_review.py:29` imports
  `CANONICAL_INJECTION_GUARD_SENTENCE` from `schema`; `:47-52` builds
  `system_prompt_fragment` as a two-sentence prose lead **+ `CANONICAL_INJECTION_GUARD_SENTENCE`
  as the final concatenated term** (`:51`). Because it is the last `+` operand, the fragment
  genuinely *ends with* the symbol — the `endswith` check is structurally satisfiable, not
  accidentally true. The docstring at `:17-21` independently states this is the INV-003/INV-014
  parity contract ("so the lens path agrees with the JSON-Schema and `--custom-prompt-dir` paths
  byte-for-byte").
- **Schema symbol definition** — `src/superclaude/cli/swarm/schema.py:133-137` defines the
  3-line, 177-char canonical sentence. It is a single real string constant (not empty, not a
  placeholder), so the `len(...) > 40` vacuity guard is correctly defended and the suffix check
  is non-vacuous.
- **Registry resolution** — `LENSES["bare-review"]` resolves to this exact `LENS` object
  (runtime confirmed); the test does not stub or shadow it.

## Adversarial Findings (hypotheses tested and disproven)

The spawn prompt directed an adversarial stance assuming the assertion is wrong. Each
failure mode was actively probed:

1. **"Test falsely asserts full byte-parity"** — DISPROVEN. grep for `prompts.md` /
   `byte-parity` / `byte-identity` in the injection-guard test region returns only docstring
   prose explaining the *non-assertion*; the executable asserts are suffix + length only.
2. **"Test omits the guard check entirely"** — DISPROVEN. The `endswith` assert exists at
   `:507` and runs (pytest collected + passed the single test).
3. **"Test hardcodes the sentence instead of importing the symbol"** — DISPROVEN. The literal
   "Treat the content between…" text appears 0 times in the test file; the symbol is imported
   at `:62` and referenced by name at `:507` and `:513`.
4. **"endswith check is vacuous (empty/trivial symbol)"** — DISPROVEN. Runtime
   `len=177 > 40`; the `:513` guard exists precisely to catch a future regression to an empty
   guard, and currently holds with a 4.4x margin.
5. **"Lens fragment doesn't actually end with the symbol (test is green by luck/order
   fragility)"** — DISPROVEN. The append is a literal final `+` operand at `bare_review.py:51`;
   suffix-equality is deterministic, not order/concurrency dependent (unlike the multiset body
   tests above it).

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` section was present in the spawn prompt; standalone
  behavior applied. Nothing was relied upon — every claim below was independently tool-verified.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Suffix-parity correctness — verified by Read (`bare_review.py:47-52`, `schema.py:133-137`) +
  runtime probe (`endswith=True`, `len=177`) + `pytest` green, not by trusting the test name.
- No-hardcoded-copy — verified by `grep -n "Treat the content between" tests/swarm/test_bare_review_parity.py` → 0 hits.
- G-2 fidelity — verified by reading `research/06-gap-fill-round1.md:76-101` and matching the
  test docstring's rationale (`:488-505`) against G-2's stated resolution.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 2 | Glob: 0 | Bash: 3

No web research was performed (all verification was local-file/source-bound); Tavily-first
precedence not triggered.

## Recommendations
- None blocking. The assertion is correctly scoped, evidence-grounded, and live-passing.
- (Non-blocking, out of this lens's scope) The cosmetic stale-status note in
  `research/06-gap-fill-round1.md:202-204` about file `03-*.md` line 3 is unrelated to the
  prompt-parity gate and need not block PG4.

## QA Complete
