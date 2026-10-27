# Unified Coverage Matrix

## File Path Verification (Step 3.1b)

| Referenced Path | Source | Status | Notes |
|---|---|---|---|
| `src/superclaude/cli/audit/reachability.py` | REQ-036, roadmap Phase 1B | NOT_FOUND | Planned new file |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | REQ-041, roadmap Phase 3 | NOT_FOUND | Planned new file |
| `tests/v3.3/conftest.py` | REQ-046 | NOT_FOUND | Planned new file |
| `tests/v3.3/test_reachability_eval.py` | REQ-039 | NOT_FOUND | Planned new file |
| `tests/v3.3/test_wiring_points_e2e.py` | D1 report | NOT_FOUND | Planned new file |
| `tests/v3.3/test_turnledger_lifecycle.py` | D2 report | NOT_FOUND | Planned new file |
| `tests/v3.3/test_gate_rollout_modes.py` | D2 report | NOT_FOUND | Planned new file |
| `tests/v3.3/test_integration_regression.py` | D3 report | NOT_FOUND | Planned new file |
| `tests/v3.3/wiring_manifest.yaml` | D3 report | NOT_FOUND | Planned new file |

**INFORMATIONAL ONLY** — this table does not change any coverage statuses.

## Coverage Totals

- Total validation surface: **62**
- COVERED: **47**
- PARTIAL: **9**
- MISSING: **4**
- CONFLICTING: **2**
- IMPLICIT: **1**

## Requirement Status Matrix

| Requirement / Concern | Status | Primary Evidence |
|---|---|---|
| FR-1.1–FR-1.18 | COVERED | roadmap.md:80-91 |
| FR-1.19 | MISSING | ABSENT |
| FR-1.20 | MISSING | ABSENT |
| FR-1.21 | MISSING | ABSENT |
| FR-2.1 | COVERED | roadmap.md:101 |
| FR-2.1a | MISSING | ABSENT |
| FR-2.2–FR-2.4 | COVERED | roadmap.md:102-104 |
| FR-3.1a–FR-3.1d | COVERED | roadmap.md:114 |
| FR-3.2a–FR-3.2d | COVERED | roadmap.md:115 |
| FR-3.3 | COVERED | roadmap.md:116 |
| FR-4.1 | PARTIAL | roadmap.md:58-61,175 |
| FR-4.2 | COVERED | roadmap.md:59-60 |
| FR-4.3 | COVERED | roadmap.md:150,160 |
| FR-4.4 | COVERED | roadmap.md:157 |
| FR-5.1 | COVERED | roadmap.md:147,156 |
| FR-5.2 | PARTIAL | roadmap.md:148-149,158 |
| FR-5.3 | IMPLICIT | roadmap.md:150 + FR-4 cross-reference |
| FR-6.1 | PARTIAL | roadmap.md:124-127 |
| FR-6.2 | PARTIAL | roadmap.md:128-129 |
| FR-7.1 | CONFLICTING | roadmap.md:47 |
| FR-7.2 | COVERED | roadmap.md:50,174 |
| FR-7.3 | CONFLICTING | roadmap.md:48-49 |
| NFR-1 | COVERED | roadmap.md:15,173 |
| NFR-2 | COVERED | roadmap.md:238 |
| NFR-3 | COVERED | roadmap.md:172 |
| NFR-5 | PARTIAL | roadmap.md:58,61,175 |
| NFR-6 | COVERED | roadmap.md:60,187 |
| SC-1 | COVERED | roadmap.md:93,248 |
| SC-2 | COVERED | roadmap.md:249 |
| SC-3 | COVERED | roadmap.md:250 |
| SC-4 | COVERED | roadmap.md:172,251 |
| SC-5 | COVERED | roadmap.md:85,252 |
| SC-6 | COVERED | roadmap.md:253 |
| SC-7 | COVERED | roadmap.md:157,254 |
| SC-8 | PARTIAL | roadmap.md:124-129,255 |
| SC-9 | COVERED | roadmap.md:157,256 |
| SC-10 | COVERED | roadmap.md:147,257 |
| SC-11 | COVERED | roadmap.md:148,258 |
| SC-12 | PARTIAL | roadmap.md:174,259 |
| Checkpoint stop conditions | PARTIAL | roadmap.md:64,133,160,179 |
| Requirement-count claim at roadmap.md:271 | CONFLICTING | roadmap.md:271 vs validation surface |
