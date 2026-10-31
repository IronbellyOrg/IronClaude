# Tier 1 observation

## Captured failing-run output
None supplied. observation_paths: []

## Execution gate
no repro available: run-site unobservable
re-run permitted: unknown. No installation, test, or generated experiment executed.

## Source observations
The destination-exists and not-force branch continues before copy at src/superclaude/cli/install_core.py:66-71. The caller passes the install force option at src/superclaude/cli/main.py:178; update passes True at src/superclaude/cli/main.py:365. These are static observations, not an incident reproduction.
