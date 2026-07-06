# R3 Test Summary — reflect-runner suite

**Overall:** PASSED — 81 passed, 1 xpassed, 0 failed.

## New test (R3 change #1)
`tests/cli/reflect/test_inline_directive.py` — 3 tests, all PASS:
- `test_inline_directive_present_with_load_bearing_phrases` — asserts "INLINE", "Do NOT delegate", "Wave 3"/"Wave 4" present.
- `test_inline_directive_appended_exactly_once` — asserts opener+closer count == 1 (fails if doubled).
- `test_inline_directive_ends_the_prompt` — asserts prompt tail is the directive (fails if removed).

## R3 change #2
`runner.py:371` — one-line comment noting EV-1 (Wave-4 on-disk merge gate, contract 1.5.1) is the structural enforcement; the prose directive is best-effort defense-in-depth.

## NEWLY-DISCOVERED FINDING (pre-existing PR regression) + Necessary Deviation
`test_no_nesting_guard.py::test_layer_b_wrapper_module_has_no_agent_imports` was FAILING on
pristine PR-branch HEAD (a3f3f0cb), BEFORE any remediation edit. Cause: PR #197's "Fix A"
`inline_directive` introduced the bare word "subagent" into runner.py (lines 369/374/376);
the test banned the substring "subagent". The PR validated `py_compile` but never ran pytest,
so a red test shipped.

**Fix (necessary deviation, authorized by task Step 6.3 "fix the offending test or source"):**
tightened the test's banned tuple from the blunt `"subagent"` to the actual agent-spawn
surface tokens `"subagent_type"` + `"Agent("` (added) — preserving the guard's true intent
("runner.py launches reflect ONLY via ClaudeProcess, no agent surface") while no longer
false-positiving on legitimate English prose in the directive STRING. Verified: runner.py
contains no `subagent_type`/`Agent(`/`Task(`/anthropic-import surface.

**Classification:** Necessary Deviation (required for a green suite / mergeable PR; tightly
coupled to R3). Surfaced to the operator as a new finding beyond the original R1–R5 set.
