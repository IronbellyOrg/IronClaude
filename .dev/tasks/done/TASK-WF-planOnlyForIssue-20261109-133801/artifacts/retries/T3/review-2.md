c69d8e1fabf2bdccfb1db74022b5ac30e7bfec8e tree=d8bc1236f5968986f7cadda0a4e8cc700290d3bd
# Parent-derived task review

## Acceptance criteria
- T3.AC1 met: src/superclaude/commands/brainstorm.md:168; artifacts/task3-spec-roundtrip.md:33-37.
- T3.AC2 met: artifacts/task3-spec-roundtrip.md:13-25.
- T3.AC3 met: src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md:57-61; artifacts/task3-spec-roundtrip.md:38-40.
- T3.AC4 unmet, F3.3: tests/skills/test_native_model_defaults.py:39-52; artifacts/task3-spec-roundtrip.md:50.
- T3.AC5 met: artifacts/task3-spec-roundtrip.md:7; tests/skills/test_native_model_defaults.py:47-52.

## Findings
F3.1 resolved.
F3.2 resolved.
F3.3 sev=blocking trigger=B1 ac=T3.AC4 at=/home/coder/workspaces/worktrees/IronClaude/issue-462/tests/skills/test_native_model_defaults.py:44 anchor="Add static assertions for each changed producer, builder, consumer and command section in tests/skills/test_native_model_defaults.py, following the existing section-slicing style." chk=y,n,n,n family=missing-consumer-parsing-section-coverage fix=Add a section-scoped contract test for Advocate Agent Instantiation's changed parse/validate instructions, asserting shared quote-aware parsing, default-marker preservation, one-time decoding and rejection of unsupported selections without testing or changing Task 4 dispatch. [covers="static assertions for each changed producer, builder, consumer and command section"] first=A2 origin=new: The diff changes a second consumer parsing section at /home/coder/workspaces/worktrees/IronClaude/issue-462/src/superclaude/skills/sc-adversarial-protocol/SKILL.md:965-971, but the grammar test inspects only the earlier input-mode parser. No delivered assertion inspects this changed consumer section. Removing its new parsing and validation instructions would leave the delivered assertions unchanged. This is missing Task 3 regression coverage for parsing, not a request to implement Task 4 advocate dispatch.

## Derivation
verdict=missing. Read-back confirms the exact AC clause at plan line 122 and the changed consumer at adversarial SKILL.md:965-971. The current focused tests cover the earlier input parser but not this second section. The new test file is absent from Q0, so origin=new, first=A2; this is not fix-induced by the command/serialization fix. F3.1 and F3.2 are resolved. Actual backend gpt-6.1-sol and tools Read/Grep verified in the complete transcript. Locality: this is a missing required test outcome (ac-outcome-missing=yes), explicitly non-local under retry.md, even though only one test file needs changing. No repair is allowed. Run Q6 extras and the adviser/revert ladder; no next task yet.
