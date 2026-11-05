observation-kind: trace

## Producers

None: the observation is a command trace, not a categorical value, so S1.6.0b producer enumeration does not apply (producer-count: n/a).

## Defect sites (informational, not producer rows)

| id | line | statement | observed in |
|---|---|---|---|
| D1 | src/superclaude/cli/install_user_setup.py:332 | `if name not in known:` skips `marketplace add` for any existing entry named ironclaude, whatever its source | tier1-observation.md case 1 |
| D2 | src/superclaude/cli/install_user_setup.py:347 and :356-374 | dependent `plugin install` / `plugin update` commands are queued up front and still run after a failed marketplace add/update | tier1-observation.md case 2 |
