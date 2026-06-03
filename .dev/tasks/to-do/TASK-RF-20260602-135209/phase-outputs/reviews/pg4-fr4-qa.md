# QA Report — Phase Gate PG-4 (Task Integrity, FR-4 search_deps)

**Topic:** FR-RV3-LOW.4 — `find_symbol(search_deps=True)` third-party API grounding into sc-reflect-protocol
**Date:** 2026-06-02
**Phase:** task-integrity (PG-4, zero-trust, adversarial)
**Fix cycle:** N/A (cycle 0 — no fixes required)

---

## Overall Verdict: PASS

All six Phase 4 outputs independently verified against source files; all six invariants hold. One MINOR cross-phase advisory recorded (a latent `yaml_list_contains` grader incompatibility inherited verbatim from the PG-3-blessed Phase-3 pattern and the research spec) — it does NOT fail PG-4 scope and was not introduced by Phase 4.

## Items Reviewed (Outputs 1–6)

| # | Output | Result | Evidence |
|---|--------|--------|----------|
| 1 | §6.1 chain step 7 (search_deps) | PASS | Read SKILL.md:377-398. Chain (fence intact) = steps 1, 2, 2a, 3, 3b, 4, 5, 6 (re-Read), 7. Step 7 `7. mcp__serena__find_symbol <symbol> search_deps:true   # third-party / dependency surface` appended AFTER re-Read step 6 (line 390). Bare-token + `<placeholder>` + right-aligned `# purpose` style. Prose @395 states the OPERATIONALIZED predicate (`a symbol whose step-2a find_declaration resolves to an <ext:…> path`) and explicitly rejects the vague "cites a third-party API by name". Names the `search_deps:lsp_unindexed` fail-open + claim stays `[INFERRED]`. Steps 1/2/2a/3/3b/4/5/6 undisturbed (order grep confirmed). NO new allowed-tools token: `grep -oE mcp__serena__*search_deps*` → none; serena cluster = 12 tools, search_deps is a param on find_symbol (correct). |
| 2 | §9.1 UC-2 contract fields | PASS | Read SKILL.md:521-558. Inside the `### 9.1 Stable contract` fence, under `# UC-2 specific` banner: `third_party_api_grounding:` nested list (`api_name`/`dep_version`/`resolution_path`) @554-557 + `third_party_api_verified: <bool>` @558, both with `# FR-4` provenance. Well-formed YAML. NO additional contract_version change in Phase 4 — `contract_version: "1.1.0"` (Phase-3 value) is the only literal (grep: 1×`: "1.1.0"`, 1×`== "1.1.0"`, no 1.2.0). |
| 3 | deviation-taxonomy.md `## Necessary` signal bullet | PASS | Read refs/deviation-taxonomy.md:40-55. Bullet @50 appended to `## Necessary` Detection-signals list, matching list style (leading `- A `, mirrors the four prior bullets). 4-category precedence undisturbed (`## Authorized`/`## Necessary`/`## Drift`/`## Regression` @26/40/56/70 + `## Classification precedence` @84 intact). |
| 4 | SKILL.md §10.2 mirror bullet | PASS | Read SKILL.md:735-749. Bullet @745 under `### 10.2 Necessary deviation` Detection signals. **Byte-identical** to deviation-taxonomy.md:50 (verified via `sed`+string-equality → IDENTICAL). §10.5 precedence `Regression > Drift > Necessary > Authorized` @781 untouched; no 5th class. Mirror pair landed in BOTH files (grep `third_party_api_verified`: taxonomy=1, SKILL=2 [§9.1 contract field + §10.2 signal]). |
| 5 | Eval scaffold `serena-search-deps/` + evals.json id 24 | PASS (with MINOR advisory — see Issue 1) | `ls`: input/diff.patch (1169B), input/tasklist.md (432B), expected.yaml (1011B). diff.patch = valid `diff --git` + `@@` hunk with the `<ext:...>` trigger (`fastapi.Depends`) AND the un-indexed-venv scenario (`from obscure_pkg import widget`) for FR-4.4. tasklist.md = `- Task N:` bullets. expected.yaml = `mode: post`/`use_case: UC-2` + FR-4 values incl. `degraded_components: [search_deps:lsp_unindexed]` + `[INFERRED]` note. evals.json: `python3 json.load` → VALID; ids 1–24 contiguous, id 24 unique (no dups). id 24: `case_dir: cases/serena-search-deps/`, `spec_ref: FR-RV3-LOW.4`, 6 assertions. All assertion types (`yaml_field_min`, `regex_present`, `yaml_list_contains`, `yaml_field`) ∈ grading_criteria AND implemented in grader.py (yaml_field@336, yaml_field_min@348, regex_present@389, yaml_list_contains@393). `yaml_field_min` confirmed present in grading_criteria. All 6 targets carry `with_skill/` prefix. |
| 6 | phase4-verify.md + phase4-sync-dev.txt accuracy | PASS | Re-ran `make verify-sync` myself → `✅ All components in sync.` exit 0 (claim accurate). Re-ran FULL markdownlint (ALL rules) HEAD-vs-current for BOTH files: SKILL.md HEAD 136 (all MD060) == current 136 (all MD060), non-MD060 = 0 at both → zero introduced of ANY rule (PG-3's MD032-class regression check satisfied); deviation-taxonomy.md HEAD 0 == current 0 → clean. Mirror-pair grep claims (taxonomy 1 / SKILL 2) reproduced exactly. phase4-sync-dev.txt shows clean sync (24 skills). All report claims accurate, no fabrication. |

## Invariants Verified

| Invariant | Result | Evidence |
|-----------|--------|----------|
| R4/A4: operationalized `<ext:…>` predicate, NOT "cites by name" | PASS | SKILL.md:395 prose uses `<ext:…>` (U+2026, matches spec) and explicitly negates the vague form. |
| search_deps predates v1.0 → no new allowed-tool token | PASS | No `mcp__serena__*search_deps*` token; serena cluster = 12 tools unchanged from Phase 3. |
| FR-4 contract-bearing, already covered by Phase-3 bump → no new Phase-4 bump | PASS | `contract_version: "1.1.0"` is the only literal; no 1.2.0. |
| Mirror edits in BOTH deviation-taxonomy.md + SKILL.md §10.2 | PASS | Byte-identical bullets at taxonomy:50 and SKILL:745. |
| `search_deps:lsp_unindexed` colon token = intentional convention (not a defect) | PASS | Present in SKILL.md:395, expected.yaml, evals.json id 24 — consistent with the Open-Questions flagged convention; not "fixed" to a hyphenated slug. |
| Pre-existing MD060 (136, SKILL.md) not a defect | PASS | HEAD and current both 136 MD060; Phase 4 introduced 0. |
| `.claude/` mirror matches src (sync correct, mirror not staged) | PASS | `diff` of FR-4 lines src-vs-.claude → MIRROR MATCHES. |

## Summary

- Outputs verified: 6 / 6
- Invariants verified: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor advisories: 1 (cross-phase, not introduced by Phase 4)
- Issues fixed in-place: 0 (none required)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR (cross-phase advisory) | `evals.json` id 24 assertion 3 (`field_path: third_party_api_grounding.0.api_name`); also id 22 (`missing_implementations.0.abstract_name_path`) | `grader.check_yaml_list_contains` resolves a dotted+indexed `field_path` then requires the resolved node to be a **list** (grader.py:182-183). An indexed path ending in a scalar key (`...0.api_name`) resolves to a **scalar string**, so the assertion returns False under the real grader. This pattern was prescribed by research §3 (04-eval-workspace-conventions.md:218-219, 329) and established in Phase 3 id 22 (PG-3-blessed). It is harmless in this task because scaffolds are never graded in-task (`with_skill/outputs/` does not exist). The correct grader type for a nested-scalar equality is `yaml_field` against a flattened key, OR the grader's `yaml_list_contains` would need a scalar-extraction branch. | NO fix applied in PG-4: (a) the assertion is a faithful reproduction of the research spec and the PG-3-accepted id 22 precedent; (b) changing it in Phase 4 would diverge id 24 from id 22 and from research without authorization; (c) it is non-blocking (scaffold). RECOMMENDATION: address grader/convention reconciliation as a single cross-phase item before any future eval run promotes these scaffolds — apply uniformly to id 22 AND id 24 (and any later nested-scalar assertions). Flag carried forward, not silently dropped. |

## Observations (non-blocking, not findings)

- **Empty Phase 4 Findings log:** The `### Phase 4 - FR-4 search_deps Findings` section of the task file (line 586) has NO timestamped entry, and the Execution Log has no Phase-4 line. The work is unambiguously present and correct (all 6 outputs verified on disk), so this is a missing log entry, not missing work. The executor SHOULD add a Phase-4 findings entry for audit completeness. Not a PG-4 gate failure (the gate verifies outputs, not log bookkeeping).

## Confidence Gate

Per-output categorization (TOTAL = 6 outputs + 7 invariants = 13 checks):

- VERIFIED (tool evidence cited): 13 — every row above cites a specific Read/grep/python/markdownlint/diff result.
- UNVERIFIABLE: 0
- UNCHECKED: 0

**Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep(via Bash grep): 11 | Glob: 0 | Bash: 9 (verify-sync ×1, markdownlint HEAD+current ×4, json/yaml parse ×3, grep batches)
(No web research performed — all claims are local-source-bound; Tavily-first rule not triggered. tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.)

Tool-engagement minimum check: (Read 9 + Bash-grep 11 + Glob 0) = 20 ≥ 13 checks. Not suspect.

## Recommendations

- PG-4 verdict is PASS — Phase 5 (FR-8 memory-retention) MAY begin.
- Executor: add the missing Phase-4 findings log entry for audit completeness.
- Cross-phase (before any scaffold promotion to a graded run): reconcile the `yaml_list_contains` nested-scalar pattern (id 22 + id 24) with `grader.check_yaml_list_contains` — either switch to `yaml_field` on a flat key or extend the grader to handle scalar-resolving `field_path`s.

## QA Complete
