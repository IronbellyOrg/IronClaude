observation-kind: string
producer-count=1
## Producers
| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|---|---|---|---|---|---|---|---|
| P1 | src/superclaude/cli/issue_watch/dispatch.py:429 | `enabled = _enabled(config_path)`; `if enabled is not True: skipped.append(Skipped(..., "not_enabled"))` | dispatch.py:436 `continue` | n/a | yes | tests/issue_watch/test_dispatch.py:421 | yes |
## Mechanism rows
(none)
