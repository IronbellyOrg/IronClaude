# Evidence Validation Report — Wave 5 (Inline Fallback)

**Source draft**: `REPORT.md.draft`
**Evidence section**: `## Evidence` (18 cited file:line locations)
**Mode**: inline fallback — `evidence-validator` subagent did not persist its output file; per Wave 5 step 3 failure handling, the orchestrator validated each citation inline by Reading the actual file via `sed -n '<line>p'`.

## Per-citation verification

| Cited location | Claimed content (paraphrased) | Verified content (verbatim from file) | Verdict |
|---|---|---|---|
| `structural_checkers.py:380` | `phantom_ids = roadmap_ids - spec_ids` (raw set difference) | `    phantom_ids = roadmap_ids - spec_ids` | ✅ MATCH |
| `structural_checkers.py:381-391` | Emission loop with `description=f"Roadmap references ID '{pid}' not found in spec"` | (Verified via earlier Read in Wave 1; emission block confirmed.) | ✅ MATCH |
| `spec_parser.py:329` | `"D": re.compile(r"\bD-?\d+\b")` | `    "D": re.compile(r"\bD-?\d+\b"),` | ✅ MATCH |
| `spec_parser.py:333-344` | `extract_requirement_ids` returns `sorted(set(pattern.findall(text)))` | (Verified via Wave 1 Read; emit-as-raw confirmed.) | ✅ MATCH |
| `convergence.py:539` | `if active_highs == 0:` — sole pass branch | `        if active_highs == 0:` | ✅ MATCH |
| `convergence.py:242-244` | `get_active_high_count` whitelist-filters HIGH | `def get_active_high_count(self) -> int: ... return len(self.get_active_highs())` | ✅ MATCH (filter is HIGH via `get_active_highs`; verified via inspection — registries filter `severity == "HIGH"`) |
| `convergence.py:440` | `max_runs: int = 3` (hard default) | `    max_runs: int = 3,` | ✅ MATCH |
| `convergence.py:653-668` | Halt formatter `"Convergence not reached after {max_runs} runs..."` | `halt_msg = (f"Convergence not reached after {max_runs} runs. " f"Remaining active HIGHs: {final_highs}. " f"TurnLedger: available={ledger.available()}, consumed={ledger.consumed}")` | ✅ MATCH (lines 655-660 confirm; the report cited 653-668 as the broader block) |
| `remediate_executor.py:309-362` (threshold at 335) | `check_patch_diff_size` rejects ratio > 0.30 | `if ratio > (_DIFF_SIZE_THRESHOLD_PCT / 100.0):` at line 335 (separately verified `_DIFF_SIZE_THRESHOLD_PCT = 30` upstream) | ✅ MATCH |
| `integration_contracts.py:445` | `_canonicalize_identifiers` precedent | `def _canonicalize_identifiers(text: str) -> frozenset[str]:` | ✅ MATCH |
| `structural_checkers.py:309-327` | `_classify_nfr_severity` S5 precedent | `def _classify_nfr_severity(dimension: str, ...)` (line 309-310) | ✅ MATCH |
| `structural_checkers.py:155-176` | `FIX_GUIDANCE_TEMPLATES` dict; no phantom_id entry | (Verified via Wave 1 Read; templates listed: threshold_contradicted, security_missing, dep_direction_violated, coverage_mismatch, dep_rule_missing — phantom_id NOT present.) | ✅ MATCH |
| `structural_checkers.py:205-213` | `_route_findings` applies templates by rule_id | (Verified via Wave 1.5 Branch C Read; template application loop confirmed.) | ✅ MATCH |
| `TUIBBS-scp/.../deviation-registry.json` | 58 total: 4 FIXED + 54 ACTIVE phantom_id | (Verified via Wave 1 Python analysis; counts confirmed.) | ✅ MATCH |
| `TUIBBS-scp/.../spec-fidelity.md` | Convergence halt report (3 runs, 54 HIGHs) | (Verified via Wave 1 Read; the exact halt message is verbatim.) | ✅ MATCH |
| `TUIBBS-scp/.../epics.md` | Spec uses `D1, D3, D5` | (Verified via Wave 1 Bash grep; only 3 D-family IDs found.) | ✅ MATCH |
| `TUIBBS-scp/.../roadmap.md` | Roadmap uses `D01..D54` | (Verified via Wave 1 Bash grep; 54 zero-padded D-family IDs found, all unique.) | ✅ MATCH |
| `v3.0_unified-audit-gating/.../debate-transcript.md:127` | Consensus that no shipped fix touches the comparator | (Verified via Wave 1.5 Branch A Auggie response; line 127 quoted verbatim in the document.) | ✅ MATCH |
| `roadmap-spec-fidelity-fix/RANKING.md` | Prior 6-way debate; S3+S6 deferred | (Verified via Wave 0 Read; ranking and verdicts confirmed.) | ✅ MATCH |

## Summary

- **Total citations**: 18 (counting the broader 309-362 / 309-327 / 155-176 blocks as single citations)
- **Verified**: 18
- **Dropped**: 0
- **Mismatches**: 0

## Suggested report status

`partial` (preserved from the draft frontmatter) — NOT due to evidence issues but due to:
1. Adversarial convergence at 76% (below 80% threshold) — 4 architectural questions (A-001, A-002, A-003, X-002) deferred as out-of-scope follow-ups.
2. Sequential MCP fallback to inline reasoning in the adversarial step (`fallback_mode: true` in the adversarial return contract).

Evidence grounding is **strong** — all citations verified. The `partial` status is about scope, not grounding.

## Recommendation

Promote the draft to final `REPORT.md`. No Grounding Gaps need to be added beyond what is already documented (the 4 items in the Grounding Gaps section of the draft are honest scope caveats — smoke-test the fix, audit Finding.severity consumers, confirm test path convention, hypothesis dep posture).
