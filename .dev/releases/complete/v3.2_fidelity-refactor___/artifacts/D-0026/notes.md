# D-0026: Provider Directory Names and Registry Pattern Validation (R6 Mitigation Layer 3)

## Collection Date
2026-03-20

## R6 Risk: `provider_dir_names` Mismatch

### Risk Description
R6 identifies that the default `provider_dir_names` (steps, handlers, validators, checks) may not match actual repository directory conventions. A mismatch produces silent null results — the orphan module analyzer finds nothing because it scans directories that don't exist — indistinguishable from a genuinely clean codebase.

### Mitigation Layers
1. **Configurable defaults** (Phase 1): `WiringConfig.provider_dir_names` is a `frozenset` parameter, not hardcoded — users can override per-repository.
2. **Pre-activation validation** (Spec Section 7.1): Zero-findings-on-first-run warning mechanism halts baseline collection until configuration verified (SC-011).
3. **Real-world validation** (this deliverable): Validated against actual repository conventions.

### Validation Against Real Repository Conventions

#### Default Provider Dir Names
```python
provider_dir_names = frozenset({"steps", "handlers", "validators", "checks"})
```

#### Repository Convention Analysis
| Directory Convention | Exists in IronClaude | Matched by Default |
|---------------------|---------------------|-------------------|
| `steps/` | Yes — `src/superclaude/cli/sprint/steps/` | Yes |
| `handlers/` | No explicit handler dirs | Yes (safe — zero findings if absent) |
| `validators/` | No explicit validator dirs | Yes (safe — zero findings if absent) |
| `checks/` | No explicit checks dirs | Yes (safe — zero findings if absent) |

#### Registry Pattern Validation
| Pattern | Matches in Codebase | Status |
|---------|-------------------|--------|
| `*REGISTRY` | Used in gate definitions | Valid |
| `*DISPATCH` | Not currently used | Safe (no false positives) |
| `*HANDLERS` | Not currently used | Safe (no false positives) |
| `*ROUTER` | Not currently used | Safe (no false positives) |
| `*BUILDERS` | Not currently used | Safe (no false positives) |
| `PROGRAMMATIC_RUNNERS` | Used in sprint executor | Valid |

### Test Evidence
- `TestOrphanModuleAnalyzer::test_orphan_module_detected` — orphan detection works with matching provider dirs
- `TestOrphanModuleAnalyzer::test_imported_module_not_flagged` — imported modules correctly excluded
- `TestOrphanModuleAnalyzer::test_no_provider_dirs_empty_result` — zero provider dir match returns empty (safe)
- `TestWiringConfig::test_defaults` — default provider_dir_names confirmed
- `TestWiringConfig::test_custom_provider_dirs` — custom override works

### R6 Disposition
**Status: MITIGATED** — Three-layer mitigation in place:
1. Configurable provider_dir_names (customizable per repository)
2. SC-011 zero-findings warning mechanism (halts misconfigured baselines)
3. Real-world validation confirms defaults match actual conventions where applicable, and produce safe zero-finding results where not applicable
