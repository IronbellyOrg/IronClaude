# D-0027: Soft Mode Readiness Assessment

## Assessment Date
2026-03-20

## Goal-5b Promotion Criteria Evaluation

### Criterion 1: False-Positive Rate Manageable via Whitelist
| Metric | Evidence | Status |
|--------|----------|--------|
| Whitelist suppression mechanism | `_apply_whitelist()` in wiring_gate.py — matches by symbol name and finding_type | Implemented |
| Shadow mode: malformed whitelist handling | Warns and skips (OQ-3) — tested in `TestWhitelistLoading` (7 tests) | PASS |
| Soft mode: strict whitelist validation | Raises `WiringConfigError` on malformed entries | PASS |
| Suppression count in report frontmatter | `whitelist_entries_applied` field confirmed in `TestEmitReport` | PASS |
| FPR burden estimate | Spec Section 5.2 notes 30-70% of unwired_callable findings in shadow mode may be re-export false positives — whitelist mechanism addresses this | Addressed |

**Assessment**: Whitelist mechanism is fully functional for FPR management. The `wiring_whitelist.yaml` suppression approach can handle expected false positive patterns (re-exports, intentional optionals) with per-entry justification.

### Criterion 2: Findings Actionable for Developers
| Finding Type | Actionability | Evidence |
|-------------|---------------|----------|
| `unwired_callable` | HIGH — directly identifies the unwired parameter, file, and line number | cli-portify fixture proves detection of real no-op bug (SC-010) |
| `orphan_module` | MEDIUM — identifies modules in provider dirs not imported by any external file | Dual evidence rule (AST + file_references) reduces false positives |
| `unwired_registry` | MEDIUM — identifies registry entries with unresolvable references | Pattern-based detection with configurable registry patterns |

**Assessment**: All finding types produce actionable output with file_path, symbol_name, line_number, and human-readable detail. The cli-portify retrospective (SC-010) confirms the gate would have caught a real production bug.

### Criterion 3: No Regression Against Legacy `ledger is None` Paths
| Test | Result |
|------|--------|
| `test_scenario_7_null_ledger_compatibility` (SC-014) | PASS — no exceptions, task status unaffected, analysis runs normally |
| Shadow mode with null ledger | No `debit_wiring()` or `credit_wiring()` calls, no crashes |

**Assessment**: Legacy null-ledger path fully backward-compatible.

### Criterion 4: Promotion Criteria Checklist
| Criterion | Status | Evidence |
|-----------|--------|----------|
| Shadow mode baseline collected | PASS | D-0025 — 82 wiring tests, 52 shadow tests, all passing |
| False-positive rate manageable | PASS | Whitelist mechanism with 7 dedicated tests |
| Findings actionable | PASS | SC-010 retrospective validates real-world detection |
| No legacy regression | PASS | SC-014 null-ledger compatibility confirmed |
| Performance within threshold | PASS | SC-009 p95 < 5s confirmed |

## Readiness Decision
**READY FOR SOFT MODE** — All Goal-5b promotion criteria satisfied with evidence from shadow mode baseline data.

### Recommended Soft Mode Configuration
```python
wiring_gate_enabled = True
wiring_gate_scope = GateScope.TASK
rollout_mode = "soft"  # Blocks on critical findings only
```

### Soft Mode Behavioral Contract
- Critical findings: block task, trigger remediation
- Major findings: warn only (logged, not blocking)
- Info findings: logged only
- Whitelist-suppressed findings: excluded from blocking count
