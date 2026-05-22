# D-0082 — Notes

## Design decisions taken in this proposal

1. **E3 reframed off OQ-8.** Design-spec §8 ties `CLAUDE_FAKE_TIME_OFFSET` to "30-min freshness tests (E3)". Because OQ-8 (env-var consumption contract) is OPEN, conditioning E3 on it would re-block this task. Reframed E3 to test the SessionStart unmatched (`session-init.sh`) hook — same milestone, same priority, no OQ-8 dependency. A freshness-staleness eval can be added as a follow-up after OQ-8 closes (out of scope for OQ-2).

2. **E14 uses the YAML callback escape hatch** (D-4). Concurrent session bursts cannot be expressed declaratively; the `callback:` field invokes a Python helper. This matches D-4's example exactly.

3. **E15 matches the design-spec §11 named case.** The "hook timeout fail-open" title in the spec example is preserved verbatim.

4. **Coverage by construction.** Every hook event in `hooks.json` is exercised by ≥1 eval among E1, E2.1–3, E3 … E15. This is the D-5 falsifiable contract: a future hook addition without a paired eval will fail `eval doctor --check-coverage`.

5. **No new Expect.* primitives required.** All 13 bodies are expressible via the v1 DSL (file/jsonl/settings/exit/stderr/stdout/duration). No schema bump.

## Alternatives considered

- **Defer OQ-2 to wait for hook expansion.** Rejected: the v1 hook surface is frozen (PR #49 close); deferring blocks the rest of M5.
- **Make E14 declarative via parameterize.** Rejected: parameterize expands to independent EvalSpec instances; coordinating concurrent spawn ordering across them requires a callback regardless.
- **Drop E15 (the design-spec failing-case demo) since it intentionally fails.** Rejected: E15 is intentionally PASS under v1 — the design-spec's "FAIL" example was a hypothetical scenario showing what failure rendering looks like. E15's actual PASS criterion is "harness reaps slow hooks → tool call completes → fail_open recorded." This is testable and deterministic.

## Sub-eval IDs vs E-numbers

E3 … E15 are integers per the FR-SCH2 regex (E1, E2.1, … E15). No sub-eval expansion proposed in this resolution. Future parameterize expansions remain available under the existing schema.

## Open follow-ups (out of scope for OQ-2 closure)

- Freshness staleness via `CLAUDE_FAKE_TIME_OFFSET` — add as E16+ once OQ-8 closes.
- Cross-hook interaction matrix (e.g., SessionStart + first UserPromptSubmit ordering) — out of scope for v1; testable in v2.
- macOS-host variants of E3 … E11 — gated on OQ-9 closure.
