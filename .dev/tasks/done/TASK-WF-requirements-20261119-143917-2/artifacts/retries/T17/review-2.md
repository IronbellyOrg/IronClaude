ead53a8a2644bd9e8c6f5e44f0b826018cc00c5c
# Review 2 of Task 17 (defaults.py), re-review of F1.1

Tests: `uv run pytest tests/issue_watch/test_defaults.py tests/issue_watch/test_module_boundaries.py -q` gave 108 passed on the second run. The first run showed one failure in test_module_boundaries.py:223 ("repos" extra). The `repos` module belongs to another task's concurrent edit, and the RULES row for it is now present at tests/issue_watch/test_module_boundaries.py:75. It is not part of Task 17 and is not a finding.

## Earlier blocking findings
F1.1 resolved

Evidence: the unknown-key branch at src/superclaude/cli/issue_watch/defaults.py:128-130 now raises `_invalid("it holds an unknown key")`. That is a fixed string and never joins the file's key names. Test tests/issue_watch/test_defaults.py (canary key test, "CANARY-17-KEY") pins it. ConfigError's contract at src/superclaude/cli/issue_watch/cycle.py:89-90 is met.

## Check that no other detail is built from file text
Every `_invalid(...)` call site in defaults.py is listed below. `_invalid` at defaults.py:62-63 prepends the module constant `DEFAULTS_FILE`.
- defaults.py:75, 85, 87: f-strings that interpolate only `key`. Each caller passes a literal from the code (`"trigger_label"`, `"approval_field"`, `"approval_option"`, `"approver_logins"`, `"allowed_owners"`, at defaults.py:133-145). Never file text.
- defaults.py:93, 96, 98, 112, 119, 121, 125, 127, 130: fixed literals.
- OSError and JSON errors are re-raised with `from None` (defaults.py:119, 125), so the original message is not chained in.
No detail is built from file text.

## AC status
- T17.AC1 met. Citations: Ti.AC1@tests/issue_watch/test_defaults.py:19 (file absent), :29 (valid file), :59 (unknown key `surprise`), :60 (bad login `-x`), :76 (`PVX_abc`, an id that does not match `PVT_`). Every path is under `tmp_path` (:14, :114, :119, :128-133, where HOME is also redirected to `tmp_path`).
- T17.AC2 met. Citation: Ti.AC2@tests/issue_watch/test_module_boundaries.py:73 (`"defaults"` rule: siblings cycle, github, predicates; the imports at defaults.py:21-23 match). The file passes: 108 passed.

## Spec behaviours, spot-checked
- Built-ins match the brief: defaults.py:28-30, plus `Approved`/`Yes` from predicates.py:17-20 and an empty map at defaults.py:58.
- The module is pure: it imports no process module (defaults.py:16-23) and reads one file (defaults.py:108-115).

## Findings
None.
