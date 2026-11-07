---
status: success
caller: sc-implement-protocol
index_state: fresh
checked_at: 2026-11-06T22:44:26Z
advisory: false
degraded: []
contract_path: ./return-contract.yaml
---

## Summary

| symbol | definition | prod shown/total | test shown/total | transitive | truncated |
|---|---|---|---|---|---|
| install_orca_skills | src/superclaude/cli/install_user_setup.py:230 | 1/1 | 4/4 | 0 | false |

## How to read this

Rows locate code and are not citations until marked call-site-verified. An empty list never proves there are no dependents. While advisory is true, nothing here may change a severity, gate or verdict.

## Readiness

MCP access, fresh own-worktree index; CLI version and pin 1.6.2 match; root/projectPath is this checkout. E-1 outcome-A. Checked 2026-11-06T22:44:26Z.

## Input

Symbol install_orca_skills, depth1, limit10, tests flag false.

## Definitions

install_orca_skills, src/superclaude/cli/install_user_setup.py:230-263, function, mapped_by name.

## Production dependents

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|
| install_user_setup | src/superclaude/cli/install_user_setup.py | 434 | 441 | call-site-verified | 1 | callers |

## Test dependents

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|
| test_orca_skills_skip_when_orca_is_absent | tests/cli/test_install_user_setup.py | 247 | null | def-line | 1 | callers |
| test_orca_skills_ignore_a_non_orca_program | tests/cli/test_install_user_setup.py | 255 | null | def-line | 1 | callers |
| test_orca_skills_request_the_three_skills | tests/cli/test_install_user_setup.py | 264 | null | def-line | 1 | callers |
| test_orca_failure_never_fails_install | tests/cli/test_install_user_setup.py | 297 | null | def-line | 1 | callers |

## Limits

Production1/1 tests4/4. No truncation; impact's queried definition removed, all other impact rows already direct callers. Call-site confirmation budget5/symbol20/run: verified1, unresolved4(test definition-only rows), dropped0. Tests not selected or executed by this read-only lookup.

## Degraded and fallbacks

None. Native Grep and Read confirmed production caller span and call. Counts are graph-discovered floors, not a claim of exhaustive dynamic references.
