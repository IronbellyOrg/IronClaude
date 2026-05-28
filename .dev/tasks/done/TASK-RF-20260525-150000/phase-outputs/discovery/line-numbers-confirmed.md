# Line Numbers Confirmed — Phase 1 Step 1.5

Verified against `/config/workspace/IronClaude/src/superclaude/cli/roadmap/integration_contracts.py` (357 lines) and `/config/workspace/IronClaude/tests/roadmap/test_integration_contracts.py` (276 lines) on 2026-05-25 16:05.

## Source: `integration_contracts.py`

| Element                           | Expected Lines | Actual Lines | Match? (Y/N) |
| --------------------------------- | -------------- | ------------ | ------------ |
| `DISPATCH_PATTERNS` list          | 20-73          | 20-73        | Y            |
| `DISPATCH_PATTERNS[0]` regex      | 22-27          | 22-27        | Y            |
| `IntegrationContract` dataclass   | 113-122        | 113-122      | Y            |
| `extract_integration_contracts`   | 153-202        | 153-202      | Y            |
| `check_roadmap_coverage`          | 205-311        | 205-311      | Y            |
| FR-MOD2.7 fallback block          | 254-297        | 254-297      | Y            |
| `impl_verbs` regex                | 270-275        | 270-275      | Y            |
| `_classify_mechanism`             | 317-344        | 317-344      | Y            |
| `_extract_identifiers`            | 347-356        | 347-356      | Y            |

## Test file: `test_integration_contracts.py`

| Element                            | Expected Lines | Actual Lines | Match? (Y/N) |
| ---------------------------------- | -------------- | ------------ | ------------ |
| `CLI_PORTIFY_BAD_ROADMAP` fixture  | ~127           | 113-127      | Y (end-line 127, append after 127) |
| `TestIntegrationAuditResult` class | ends ~277      | 263-276 (ends at line 276) | Y (close — append after 276) |

**All line citations confirmed accurate**
