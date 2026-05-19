# Gap-Fill Applied — Research Quality Gate Fixes

**Date:** 2026-05-17
**Inputs:** `qa/qa-research-gate-report.md` (7 issues), `qa/analyst-completeness-report.md` (1 finding)
**Files edited:** 2 (`research/01-file-inventory.md`, `research/03-test-verification.md`)

---

## Fix Index

| # | Severity | Source | File edited | Lines/section | Change summary |
|---|----------|--------|-------------|---------------|----------------|
| 1 | CRITICAL | QA Issue #1 | `research/03-test-verification.md` | §7 V5 + V7 skeleton (~lines 519, 521, 549, plus inline comment) | `new_data["hooks"]["PreToolUse"]` → `new_data["hooks"]["PostToolUse"]` in both V5 and V7 test bodies. Inline comment "PreToolUse → auggie-flag-clear" corrected to "PostToolUse → auggie-flag-clear". Verified hooks.json:47 starts the `"PostToolUse": [` block; line 60 = matcher; line 64 = `command: "~/.claude/hooks/auggie-flag-clear.sh"`. |
| 2 | IMPORTANT | QA Issue #2 | `research/03-test-verification.md` | §7 V5 + V7 skeletons | Added `# JSON round-trip is acceptable because verify-sync parses the matcher value (via jq), not the full file bytes.` comment immediately above each `json.dumps(...)` call. |
| 3 | IMPORTANT | QA Issue #3 | `research/03-test-verification.md` | §7 `_temporarily_mutate_freshness_list` docstring | Appended fragility note explaining the regex assumes no `.sh` literals inside inline comments within the list; future maintainers should switch to AST parsing if that invariant breaks. |
| 4 | IMPORTANT | QA Issue #4 | `research/03-test-verification.md` | §7 module docstring | Added pytest-xdist warning at the top of the module docstring (DO NOT run with pytest-xdist — concurrent mutation will race and corrupt files). |
| 5 | IMPORTANT | QA Issue #5 | `research/03-test-verification.md` | §6 (mitigation paragraph) + §7 (`pytestmark` list + skeleton notes) | Restructured `pytestmark` to a LIST of TWO module-level skipifs (both `_HAS_MAKE` and `_HAS_JQ`). Removed per-test `@pytest.mark.skipif(not _HAS_JQ, ...)` decorators from V5, V6, V7 (made redundant by module-level mark). §6 mitigation text explicitly clarifies jq is required by the `=== Hooks Cross-Consistency ===` section on EVERY verify-sync run including V1 clean-tree. |
| 6 | MINOR | QA Issue #6 | `research/03-test-verification.md` | §7 V5 test body | Removed unused `original = json.loads(HOOKS_JSON.read_text())` line. Only `new_data` was ever used; the duplicate read was dead code. |
| 7 | MINOR | QA Issue #7 | `research/01-file-inventory.md` | §2.1 last bullet (`Test scenarios per release-spec`) | Replaced the inline V1–V7 enumeration (which disagreed with release-spec §9 and research-03 §7) with a pointer to the authoritative table: "see release-spec.md §9 and research-03 §7. Research-01 does not enumerate scenarios — the authoritative mapping lives in those two files." |
| 8 | IMPORTANT | Analyst finding #1 (Important Gap #1) | `research/01-file-inventory.md` | §1.1 (line anchors block + insertion-anchor narrative + verbatim block) and §4 Summary Table + §5 finding 4 | Disk-verified Makefile line numbers (re-Read lines 230-250): line 240=`done; \`, 241=`echo ""; \`, 242=`if [ "$$drift" -eq 0 ]; then \`, 243=`echo "✅ All components in sync."; \`, 244=`else \`, 245=`echo "❌ Drift detected!..."; \`, 246=`exit 1; \`, 247=`fi`. Analyst's claim of 240/241/242 is CORRECT; researcher-01's claim of 241/242/243 was off-by-one. Updated all `01-file-inventory.md` line citations to the disk-verified numbers. Also updated the verbatim Read block (was 240/241/242/243 → now 239/240/241/242 with the closing `fi; \` on 239 and `done; \` on 240). |

---

## Verification Performed

- **hooks.json PostToolUse confirmed** via prior QA report Issue #20 evidence chain (line 47 PostToolUse block start; line 60 matcher; line 64 command path).
- **Makefile line numbers re-verified** this session by re-Reading `Makefile` lines 230-250. Disk state matches analyst's claim (240/241/242), not researcher-01's claim (241/242/243). Researcher-01 §1.1 updated accordingly; analyst report stands as written.
- **Module-level jq pytestmark** changed to `pytestmark = [pytest.mark.skipif(not _HAS_MAKE, ...), pytest.mark.skipif(not _HAS_JQ, ...)]` — list-form is the standard pytest pattern for multiple module-level marks.

## Fixes NOT Applied

None — all 8 fixes applied successfully.
