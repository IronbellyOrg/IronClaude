c69d8e1fabf2bdccfb1db74022b5ac30e7bfec8e
# Blocking-family probe

## stale-implicit-family-rotation
Defect form: omitted-model examples and boundaries still promise an automatic three-family rotation.

Search command (literal, read-only):
```text
grep -n -E -e '3 active aliases|3 models|Serialization|Escape backslashes|serialization:|default:architect' -- src/superclaude/commands/brainstorm.md src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md src/superclaude/skills/sc-brainstorm-protocol/SKILL.md src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md src/superclaude/skills/sc-adversarial-protocol/SKILL.md src/superclaude/commands/adversarial.md tests/skills/test_brainstorm_protocol.py tests/skills/test_native_model_defaults.py plugins/superclaude/commands/brainstorm.md
```
Before-output: brainstorm command lines 109,168,177 contain the three stale claims; plugin command lines 106,152,161 repeat them. Builder lines 63-67,103-104,113,160-163 and producer line 252 carry default examples; adversarial lines 74-75 accept them. Coupled sites: the source command example and both boundary bullets require the same rule. The plugin mirror is explicitly reserved for Task 5 and remains unchanged here. The adversarial serialization key at 2467 describes dependency-DAG YAML, not agent-spec serialization. The selection boundary regression belongs in the focused test file.

after: saved command re-run after the fix. No stale claims remain in the source command. The focused test now contains the stale strings only as forbidden-value assertions at line 85. The plugin hits remain at 106,152,161, deferred to Task 5 as required. Builder/producer default and escaping locations remain intact. Serialization regression assertions now appear at tests/skills/test_native_model_defaults.py:55-75. The full serialization-family recheck also found the shared decode-once rules at agent-specs.md:60-61 and adversarial SKILL.md:77,585,967; no second parser was added.

## missing-serialization-contract-coverage
Defect form: static tests inspect validation and selection, but not either changed serialization section.

Search command (literal, read-only):
```text
grep -n -E -i -e 'serializ|escape backslashes|backslash' -- tests/skills/test_native_model_defaults.py tests/skills/test_brainstorm_protocol.py src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md src/superclaude/skills/sc-brainstorm-protocol/SKILL.md src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md src/superclaude/skills/sc-adversarial-protocol/SKILL.md src/superclaude/commands/brainstorm.md src/superclaude/commands/adversarial.md
```
Before-output: neither test file contains serialization or backslash assertions (earlier test-only grep exit 1). Builder serialization is at 97-114, escaping at 106; producer serialization is at 234-239, escaping at 237. Shared validation at builder 125 describes decode-once handling. Coupled sites: assert both sections independently, plus producer final output at 249-253, so default examples and escaping remain pinned without a second parser. Adversarial DAG serialization is unrelated.

after: saved command re-run after the fix. No stale claims remain in the source command. The focused test now contains the stale strings only as forbidden-value assertions at line 85. The plugin hits remain at 106,152,161, deferred to Task 5 as required. Builder/producer default and escaping locations remain intact. Serialization regression assertions now appear at tests/skills/test_native_model_defaults.py:55-75. The full serialization-family recheck also found the shared decode-once rules at agent-specs.md:60-61 and adversarial SKILL.md:77,585,967; no second parser was added.
