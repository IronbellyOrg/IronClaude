VERDICT: FAIL

# QA Report — Test-Assertion Strength (Tavily MCP 0.2.x upgrade)

**Topic:** TASK-RF-tavily-mcp-0-2-x-20260623-010952 — test suite assertion strength
**Date:** 2026-06-23
**Phase:** report-validation (test-quality lens)
**Lens:** TEST-ASSERTION STRENGTH (adversarial; mutation-driven)
**Fix authorization:** FALSE (report only)

---

## Overall Verdict: FAIL

One CRITICAL defect: `tests/docs/test_tavily_doc_alignment.py` (all 4 tests) is **vacuously green** when run from any path containing a `.dev` / `.claude` / `dist` / `.venv` ancestor directory — which is the project's mandated worktree location (`.dev/worktrees/`). In this worktree it scans **0 files** and would pass even with the entire C8 source change reverted. The other 8 files are strong and mutation-proven.

---

## CRITICAL FINDING C1 — doc-alignment scans 0 files from the worktree (false green)

**Location:** `tests/docs/test_tavily_doc_alignment.py:41-52` (`_iter_text_files`), exclusion check at line 47:
`if any(part in _EXCLUDE_DIRS for part in p.parts): continue`

**Root cause:** The exclusion walks `p.parts` (the **absolute** path), not the path **relative to `_REPO`**. `_REPO` resolves to `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade`, whose own ancestry contains `.dev` — a member of `_EXCLUDE_DIRS = {.dev, .claude, dist, node_modules, .venv, __pycache__, .git}`. Therefore EVERY file under `src/superclaude` and `docs` is excluded, and `_iter_text_files` yields nothing.

**Evidence (verified):**
- Direct count of yielded files from this worktree: **0** (computed by replaying the test's exact iterator logic; `_REPO.parts` = `('/','config','workspace','IronClaude','.dev','worktrees','TavilyUpgrade')`, `.dev in parts == True`).
- Mutation proof: set `install_mcp.py` command to `tavily-mcp@0.1.2`; `test_tavily_version_single_pin` **PASSED** (should have failed). Manual replay of the scan returned `BAD entries found: []`.
- CI-sim counter-proof: copied the test + `install_mcp.py` to a clean `/tmp/citest` (no `.dev` ancestor), applied the same `@0.1.2` mutation → `test_tavily_version_single_pin` **FAILED** correctly with `[('src/superclaude/cli/install_mcp.py', '0.1.2')]`.

**Impact:** In the worktree (the canonical dev/CI-from-worktree location per CLAUDE.md), all four guards provide ZERO protection:
- `test_tavily_version_single_pin` — would not catch `@latest` / `@0.1.2` anywhere in src+docs.
- `test_no_stale_mcp_tavily_token` — would not catch a stale `mcp.tavily` token.
- `test_no_tavily_json_references` — would not catch a re-introduced `tavily.json` reference.
- `test_docs_no_default_params_duplication` — would not catch DEFAULT_PARAMETERS duplication in docs.

The `mcp.tavily` negative-lookahead regex itself is correct (verified: `mcp.tavily.com` does NOT match; bare `mcp.tavily` DOES match) — but it is never exercised here because the file set is empty.

**Required fix (report-only; not applied):** Make the exclude check relative to the scan root, e.g. compute `rel = p.relative_to(root)` and test `any(part in _EXCLUDE_DIRS for part in rel.parts)`; or iterate with a pruned walk. Add a guard assertion that `_iter_text_files` yields > 0 files (a self-test against vacuous passing) so this regression is caught regardless of checkout location.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All tests read ACTUAL source (no bypass) | PASS w/ 1 exception | 8/9 files read real registry/manifest/file content; doc-alignment reads real content but iterator yields 0 in worktree (C1) |
| 2 | install argv: DEFAULT_PARAMETERS token + `-e` precedence + 0.2.20 + no subprocess | PASS | Source `install_mcp.py:556-565,610-638` matches; monkeypatch targets `_run_command`/`check_mcp_server_installed`/`prompt_for_api_key` all real; mutation (mask no-op) → test FAILED |
| 3 | parity: referenced⊆declared + exact equality for documenting files; rf no map/crawl | PASS | Mutation: prose `tavily-map` in rf-analyst → both subset + rf_no_map_crawl FAILED; removing declared `search` from rf-qa frontmatter → subset + exact-parity FAILED |
| 4 | doc-alignment version pin / stale-token / scope exclusion | FAIL | C1: 0 files scanned in worktree; lookahead regex correct but never exercised; CI-sim proves it works only without `.dev` ancestor |
| 5 | eval E16: requires mcp_server.tavily + expect_tool_call search + failure_mode skip via loader | PASS | Mutations: drop capability spec → 3 tests FAILED; wrong expect_tool_call → FAILED; failure_mode fail → FAILED; loads via `validate_manifest`/`resolve_suite_manifest` (real loader path) |
| 6 | capability roster gained mcp_server.tavily | PASS | `_DEFAULT_CAPABILITY_SPECS` real = exactly the 8 asserted names; removal mutation → roster test FAILED |
| 7 | No assert True / empty / swallowing except / always-pass | PASS | Grep across all 9 files: NONE; only try/except is a narrow read-guard (doc-alignment:56-58) returning "" on UnicodeDecodeError/OSError — acceptable |

## Summary
- Checks passed: 6 / 7 lens checks
- Checks failed: 1 (doc-alignment, CRITICAL)
- Critical issues: 1
- Issues fixed in-place: 0 (fix_authorization FALSE)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | tests/docs/test_tavily_doc_alignment.py:47 | `_EXCLUDE_DIRS` matched against absolute `p.parts`; worktree's `.dev` ancestor zeroes the scan → all 4 tests vacuously pass in `.dev/worktrees/` | Use `p.relative_to(root).parts` for the exclude check; add a `yield count > 0` self-guard assertion |
| 2 | MINOR | tests/cli/test_install_mcp_tavily.py:113-118 | `test_live_tavily_search_smoke` re-asserts the same `@0.2.20` pin as `test_tavily_registry_pins_0_2_20`; only adds value when `TAVILY_API_KEY` is set (skipped in CI) | Acceptable as a presence gate; no action required (noted for completeness) |

## Per-Test "What Mutation It Catches" (verified by execution)
- test_tavily_registry_pins_0_2_20 — catches version pin drift (`@0.1.2` → FAIL). VERIFIED.
- test_default_parameters_field — catches a changed/removed `default_parameters` dict (asserts exact `{search_depth:basic,max_results:10}` against real registry). VERIFIED by source read.
- test_tavily_json_absent — catches re-introduction of the deleted `src/superclaude/mcp/configs/tavily.json` (confirmed ABSENT). VERIFIED.
- test_default_parameters_propagated — catches loss of the compact `-e DEFAULT_PARAMETERS=...` token, broken `-e` precedence, missing `0.2.20`, or wrong `claude mcp add` prefix; proves no real subprocess (intercepts `_run_command`). Source `install_mcp.py:556-638` matches exactly.
- test_api_key_never_in_logged_command — catches a broken mask (mutated mask→no-op leaked the secret → FAIL). VERIFIED.
- test_prose_tavily_ids_are_declared — catches prose referencing an undeclared `mcp__tavily__*` (added `tavily-map` to rf-analyst prose → FAIL; removed declared `search` from rf-qa → FAIL). VERIFIED.
- test_documenting_files_have_exact_parity — catches declared≠referenced in documenting files (removed declared `search` from rf-qa → FAIL). VERIFIED.
- test_rf_no_map_crawl — catches any rf-* gaining map/crawl (added `tavily-map` to rf-analyst → FAIL). VERIFIED.
- test_rf_fallback_provenance_present — catches loss of Tavily-first + WebSearch fallback language in any rf-* (all 8 rf files confirmed carry search + Tfirst + WebSearch). VERIFIED by grep.
- test_each_depth_profile_names_concrete_params_and_tools — catches a profile row losing concrete basic/advanced values or tool names. Source rows 68-71 verified.
- test_advanced_only_with_gating_language — catches quick/standard gaining `advanced` or loss of the gating sentence (set quick→advanced → FAIL). VERIFIED.
- test_discovery_caps_and_crawl_truncation_present — catches loss of `maps=2`/`crawls=1`/50-URL cap. Source 77-78,93-94,98 verified.
- test_map_and_crawl_tool_ids_present — catches loss of the map/crawl tool ids. Source 93-94 verified.
- test_research_command_no_param_duplication — catches a Tavily param leaking into research.md (appended `search_depth:` → FAIL). VERIFIED.
- test_research_tiers_match_config — catches tier name/order drift between research.md and RESEARCH_CONFIG.md. Source Adaptive-Depth section verified (Quick/Standard/Deep/Exhaustive, lowercased by the test).
- test_brainstorm_no_tavily_param_duplication — catches a Tavily param or map/crawl token entering Wave-2A (injected `tavily-map` in section → FAIL). VERIFIED.
- test_tier2_tool_id_parity — catches extract/map/crawl entering the 4 C5 files (added `tavily-extract` to reflect SKILL → FAIL). VERIFIED.
- test_rate_cap_intact — catches loss of the ≤2-query Tier-2 cap (source troubleshoot:335 verified).
- test_fail_open_intact — catches loss of fail-open/degraded language in troubleshoot+reflect SKILLs.
- test_troubleshoot_search_depth_advanced — catches loss of `search_depth: advanced` override OR a per-call param leaking into reflect (set advanced→basic → FAIL). VERIFIED.
- test_tavily_version_single_pin — INTENDED to catch any `tavily-mcp@<not 0.2.20>`; **DEFEATED in worktree (C1)** — passed under `@0.1.2`; works only from a non-`.dev` path (CI-sim FAIL proven).
- test_no_stale_mcp_tavily_token — intended to catch a bare `mcp.tavily` token; regex correct but **never exercised in worktree (C1)**.
- test_no_tavily_json_references — intended to catch re-added tavily.json refs; **never exercised in worktree (C1)**.
- test_docs_no_default_params_duplication — intended to catch DEFAULT_PARAMETERS duplication in docs/; **never exercised in worktree (C1)**.
- test_capabilities_registers_mcp_server_tavily / test_real_suite_has_tavily_capability_and_verification_eval / test_tavily_eval_gated_to_skip_without_key — catch removal of the capability, wrong E16 tool, or non-skip failure_mode (all three mutations → FAIL). VERIFIED via real loader path.
- test_capability_gates roster — catches roster drift (asserts exact 8-name set; removal of tavily spec → FAIL). VERIFIED.

## Confidence
- Verified: 7/7 lens checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 9 | Grep: ~15 | Glob: 0 | Bash: ~22 (incl. 12 live mutation runs + 1 CI-sim)
- Note: every "VERIFIED" claim above is backed by an executed mutation that flipped the named test red, or a direct source read of the asserted token.

## Recommendations
1. Fix C1 before merge: change the doc-alignment exclude check to operate on `relative_to(root).parts`, and add a vacuous-scan guard. This is the single blocker.
2. After the fix, re-run from the worktree and confirm `test_tavily_version_single_pin` FAILS under a temporary `@0.1.2` mutation (currently it does not).
3. No other changes required — the remaining 8 files are mutation-proven strong.

## QA Complete
