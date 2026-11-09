c69d8e1fabf2bdccfb1db74022b5ac30e7bfec8e
# Blocking-family probe

## missing-consumer-parsing-section-coverage
Defect form: changed consumer parse/validate section has no section-scoped regression assertion.

Command:
```text
grep -n -F -e 'agent_spec_parsing' -e 'Advocate Agent Instantiation' -e 'preserve default marker' -- src/superclaude/skills/sc-adversarial-protocol/SKILL.md tests/skills/test_native_model_defaults.py tests/skills/test_brainstorm_protocol.py src/superclaude/skills/sc-brainstorm-protocol/SKILL.md src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md src/superclaude/commands/brainstorm.md src/superclaude/commands/adversarial.md
```
Before-output: adversarial SKILL.md:582,587,957,965,966; focused tests:44 only (the earlier input parser slice). No test slice covers Advocate Agent Instantiation. Coupled sites: the shared input-mode grammar, second consumer parse/validate section and generation grammar need an explicit section-to-test inventory. No Task 4 dispatch edit is implicated.

Locality: missing required outcome, therefore non-local under retry.md. Escalate with no in-place repair.
