# Reviewer Card 2 — QA / Coverage (qwen3.6-plus, haiku-class)

**Persona:** quality-engineer · **Stance:** adversarial · **Self-confidence:** 0.88 · **Calibrated:** 0.90

**VERDICT:** pass-with-concerns

## Findings
1. (HIGH→reclassified MEDIUM) Test asserts only string presence; `env -u WRONG_VAR` substitution partially guarded by the 2nd assertion. real_gap: yes, blocking: no.
2. (HIGH→MEDIUM) String-presence on markdown ≠ behavioral proof. For a doc-only (model-executed) fix surface this is the appropriate guard; tests 1-5 cover the Python recursion-breaker behavior. real_gap: yes, blocking: no.
3. (MEDIUM) Anchor fragility: `text.index("### 6.1.1 ...")` / `text.index("### 6.2", start)` throw ValueError on heading renumber/reword/reformat. real_gap: yes, blocking: no.
4. (LOW→escalated) **`_MARKER` appears in TWO places in §6.1.1** — control (b) line 494 AND control (i) line 501. `assert _MARKER in envelope` is dead signal; relies entirely on the 2nd assertion. real_gap: yes.
5. (LOW) `parents[3]` correct for tests/cli/reflect/ → repo root. real_gap: no.
6. (MEDIUM) 2nd assertion necessary-not-sufficient: the literal `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` also appears in control (b)'s backticked cross-reference, so deleting control (i) alone leaves BOTH assertions True.

**TEST_ADEQUACY:** pass-with-concerns — adequate as a doc-level regression guard, but should assert on control (i)'s bullet, not bare substring presence in the whole section.

**STRONGEST_OBJECTION (independently re-verified — see REPORT §4):** Control (b) at SKILL.md:494 contains the exact string `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` in backticks. If control (i) were deleted entirely, BOTH `assert _MARKER in envelope` AND `assert f"env -u {_MARKER}" in envelope` still pass → the test FALSE-PASSES on surgical removal of the fix. Fix: assert on `"**(i) Wrapper-marker strip"` or require co-occurrence with the execution imperative "MUST be executed as the fixed protocol-authored wrapper".

> ORCHESTRATOR NOTE: Empirically confirmed by simulation (delete control-(i) bullet → both assertions remain True). This is the single highest-value finding of the audit. Classified as a non-blocking quality recommendation (the work still CONFORMS to KO4 as literally written); basis for the Tier-3 remediation offer.
