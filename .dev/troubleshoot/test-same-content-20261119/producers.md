observation-kind: string
producer-count: not categorical

The observed datum is a boolean assertion result (`same_content(a, b)` returned True where False was expected), not an enum token, so there is no producer menu. Single producer of the value: `src/superclaude/cli/install_keep.py:21` (`return filecmp.cmp(a, b, shallow=False)`), the only `return` in the `try`; the `except OSError` branch returns False at :23 and is not taken (both files exist).

## Producers

| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|---|---|---|---|---|---|---|---|
| P1 | src/superclaude/cli/install_keep.py:21 | `return filecmp.cmp(a, b, shallow=False)` | return at :21 | n/a | yes | pytest assertion at tests/cli/test_install_keep.py:43 | yes |
