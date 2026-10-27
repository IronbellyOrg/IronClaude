# D-0025: Pre-Activation Safeguards

## Deliverable
Pre-activation safeguard checks in sprint executor:
1. Zero-match warning when >50 files scanned but 0 findings produced
2. Whitelist validation confirming whitelist file is parseable
3. `provider_dir_names` configuration sanity check

## Implementation
- `run_wiring_safeguard_checks(config, report=None)` function in `executor.py`
- All checks produce WARNING log messages only — they never block execution
- Returns list of warning strings for testability

## Safeguard Details
| Check | Trigger | Severity |
|-------|---------|----------|
| Zero-match | files_analyzed > 50 AND total_findings == 0 | WARNING |
| Whitelist | YAML parse failure or non-mapping type | WARNING |
| Provider dirs | Configured directory name not found under source_dir | WARNING |

## Evidence
```
T05.03 PASS: All pre-activation safeguards work correctly
```
