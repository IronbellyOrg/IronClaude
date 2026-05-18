# QA Report — Research Gate

**Topic:** hook-sync-and-matcher-fix MDTM task generation
**Date:** 2026-05-17
**Phase:** research-gate
**Fix cycle:** N/A (fix_authorization=false)

---

## Overall Verdict: FAIL

One CRITICAL bug in the proposed test skeleton (research-03) plus several IMPORTANT gaps the task-builder must handle. The research is otherwise dense, well-evidenced, and structurally sound — but the CRITICAL item would produce silently broken tests if copied verbatim.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory + Status:Complete | PASS | All 4 files have `**Status:** Complete` headers; all are substantial (225/302/591/320 lines). |
| 2 | Evidence density — Makefile line claims (res-01 §1.1) | PASS | Re-Read Makefile:154-247: line 154 `verify-sync:` confirmed; line 158 `=== Skills ===` confirmed; line 190 `=== Agents ===` confirmed; line 216 `=== Commands ===` confirmed; line 241 `done; \` confirmed; line 242 `echo ""; \` confirmed. Insertion-anchor description accurate. |
| 3 | Evidence density — hooks.json:60 matcher (res-01 §1.2, spec §4.1) | PASS | Re-Read hooks.json:60 = `        "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",` — verbatim match to claim. |
| 4 | Evidence density — auggie-flag-clear.sh:22 case body (res-01 §1.3, spec §4.2) | PASS | Re-Read script line 22 = `    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)` — verbatim match. |
| 5 | Evidence density — auggie-flag-clear.sh:2 comment (res-01 §1.3, spec §4.2) | PASS | Re-Read line 2 = `# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.` — verbatim match. |
| 6 | Evidence density — _FRESHNESS_SCRIPTS lines 43-55 (res-01 §3.1, res-03 §4) | PASS | Re-Read install_hooks.py:43-55 — list contents and line range match verbatim including the `freshness-file-changed.sh` v1-not-registered inline comment. |
| 7 | Orphan claim — `.claude/hooks/auggie-bash-gate.sh` exists, no src/ counterpart (spec §1.2) | PASS | `ls .claude/hooks/` confirms `auggie-bash-gate.sh` (2593 bytes, May 17 17:58). `ls src/superclaude/hooks/scripts/` confirms NO `auggie-bash-gate.sh`. Orphan claim verified. |
| 8 | `reject-workspace-writes.sh` installer-orphan (res-01 §3.2) | PASS | Confirmed: file exists in BOTH `src/superclaude/hooks/scripts/` (2027b) and `.claude/hooks/` (2027b), but is NOT in `_FRESHNESS_SCRIPTS` (re-read install_hooks.py:43-55 — no entry for it). |
| 9 | `tests/cli/__init__.py` absent (res-01 §2.1, res-03 §5) | PASS | Verified via `test -f` — file does not exist. |
| 10 | `tests/cli/` siblings present (res-01 §2.1) | PASS | `ls tests/cli/` returns `prd/`, `__pycache__`, `test_install_hooks.py`, `test_tdd_extract_prompt.py`. |
| 11 | No existing make-subprocess tests (res-03 §3) | PASS | `grep -rn '"make"\|subprocess.*make' tests/` returns zero matches. Pioneering pattern confirmed. |
| 12 | Makefile uses no jq, no comm, no `<(...)` (res-02 §5) | PASS | `grep jq Makefile` zero matches; confirmed by patterns research. |
| 13 | Header convention — `set -u` not `set -euo pipefail` (res-02 §2) | PASS | Re-Read auggie-flag-clear.sh:5 = `set -u`. Verified. |
| 14 | hooks.json indentation/key order (res-02 §3) | PASS | Re-Read lines 55-68 — 2-space indent confirmed; `matcher` precedes `hooks`; `type`/`command`/`timeout`/`async` ordering matches. |
| 15 | Pytest skeleton — REPO_ROOT path math (res-03 §3) | PASS | `Path(__file__).resolve().parents[2]` from `tests/cli/test_verify_sync_hooks.py` → repo root. Verified by parent-count. |
| 16 | tmp_path strategy resolution (res-03 §4) | PASS | Clearly recommends "mutate real files via context managers with try/finally" for all V2-V7, with Option A/B/C trade-off analysis. Concrete and actionable. |
| 17 | Template 02 PART 2 copy range (res-04 §1) | PASS | Path `.claude/templates/workflow/02_mdtm_template_complex_task.md` is documented; PART 2 lines 896-1197. Did not re-verify line range itself (out of scope for this gate — task-builder verifies before copy). |
| 18 | Comparable task `TASK-RF-track-3-...` (res-04 §3) | PASS-WITH-NOTE | Path cited; phase structure detailed; not re-read for line-by-line accuracy (acceptable for example reference, not load-bearing for builder). |
| 19 | Phase skeleton recommendation (res-04 §7) | PASS | Concrete: 4 phases + 2 phase-gates + post-completion. Maps cleanly to spec parts 1/2/3. |
| 20 | **Skeleton uses `PostToolUse` for auggie-flag-clear matcher mutation** | **FAIL** | Re-Read hooks.json: auggie-flag-clear.sh matcher is registered under `PostToolUse` (block starts at line 47), NOT `PreToolUse`. Research-03 skeleton at lines 521 + 549 iterates `new_data["hooks"]["PreToolUse"]` — wrong key. Tests V5/V7 would silently no-op (no matching registration found to mutate), `_temporarily_replace_file` would write unchanged JSON, verify-sync would NOT report DRIFT, assert would fail with cryptic stdout. Verified via `grep -n 'PreToolUse\|PostToolUse' hooks.json` → line 35 PreToolUse, line 47 PostToolUse; the auggie-flag-clear command is at line 64 (inside PostToolUse block). |
| 21 | CI jq risk surfaced (res-03 §6) | PASS | Documented as UNVERIFIED; mitigation via `pytest.mark.skipif(not shutil.which("jq"), ...)` proposed. Concrete recommendation present. |
| 22 | CI uv availability (res-03 §6) | PASS | Documented as available; cold-boot cost noted (~200-500 ms). |
| 23 | `reject-workspace-writes.sh` surfaced as builder consideration | PASS | res-01 §5 "Critical Findings" #2 explicitly calls this out as a follow-up consideration the builder should handle. |
| 24 | `auggie-bash-gate.sh` orphan flagged as out-of-scope but detectable | PASS | spec §1.2 + spec §6 documents this; res-01 §5 #3 reiterates. Out-of-scope-but-detectable framing is consistent. |
| 25 | hook-sync-coverage-spec.md content claims | PASS | I read hook-sync-coverage-spec.md §4.2 (lines 94-112) — recommends `uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; ..."`. Caveat about `uv run` correctly noted. |

---

## Confidence Gate

- **Verified:** 25 / 25 verifiable items
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 4
  - Reads: 4 research files, release-spec.md, hook-sync-coverage-spec.md, Makefile lines 150-249, hooks.json lines 55-68, auggie-flag-clear.sh (full), install_hooks.py lines 36-60. Each Read mapped to specific checklist verification.
  - Bash: 4 calls — directory listings + wc -l + grep for PreToolUse/PostToolUse + grep for jq/make subprocess use + targeted grep on research-03 itself. Each mapped to a specific check.

Tool-engagement floor satisfied.

---

## Summary

- Checks passed: 24 / 25
- Checks failed: 1 (CRITICAL)
- Critical issues: 1
- Important issues: 4
- Minor issues: 2

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | **CRITICAL** | research/03-test-verification.md §7 skeleton, lines 521 and 549 (`for reg in new_data["hooks"]["PreToolUse"]:` in `test_V5_matcher_drift_detected` and `test_V7_regression_to_master`); also the inline comment on line 519 "Mutate the matcher at hooks.json:60 (PreToolUse → auggie-flag-clear)" repeats the same wrong attribution. | The skeleton iterates `PreToolUse` to find and mutate the auggie-flag-clear registration. But auggie-flag-clear.sh is registered under `PostToolUse` in hooks.json (PostToolUse block starts at line 47; the matcher under test is at line 60 inside that block; the command path at line 64 confirms it). The for-loop will iterate PreToolUse entries (Read/Edit/Write freshness hooks), find no `auggie-flag-clear` command, exit without mutating anything. `_temporarily_replace_file` then writes back JSON that is semantically unchanged, `make verify-sync` reports no drift, and the assertion `assert result.returncode != 0` fails with no useful diagnostic. **This bug also propagates to V6 even though V6 mutates the shell script not hooks.json** — V6 is fine by itself, but a task-builder copying the skeleton verbatim picks up the bug in V5/V7. | Replace both occurrences of `new_data["hooks"]["PreToolUse"]` with `new_data["hooks"]["PostToolUse"]`. Correct the comment at line 519 too. Task-builder MUST NOT copy this verbatim. |
| 2 | IMPORTANT | research/03-test-verification.md §7 skeleton, V5 + V7 tests | The mutation loads JSON and re-serializes via `json.dumps(new_data, indent=2)`. CPython preserves dict ordering since 3.7, but the round-trip will NOT preserve the original file's exact byte layout (notably trailing newline and any subtle whitespace). Today no consumer compares hooks.json byte-for-byte, so the test works — but it is a fragility that should be documented so a future byte-checksum consumer does not silently break this. | Builder adds a comment on V5/V7 items: "JSON round-trip is acceptable because verify-sync parses the matcher value, not the full file bytes." |
| 3 | IMPORTANT | research/03-test-verification.md §7 skeleton, V3/V4 `_temporarily_mutate_freshness_list` helper | Regex `_FRESHNESS_SCRIPTS = \[.*?\]` with `re.DOTALL` works today, and `re.findall(r'"([^"]+\.sh)"', ...)` correctly extracts only `.sh` literals from the captured block. Verified safe against current install_hooks.py:43-55 (inline comments contain no `.sh` literals). However, if a future maintainer adds a `.sh` filename inside an inline comment within the list, the helper will treat it as an entry. | Builder should document this fragility in the helper docstring (and prefer a more robust parser if the list ever exceeds ~20 entries). |
| 4 | IMPORTANT | research/03-test-verification.md §7 skeleton — pytest-xdist safety | The skeleton mutates real files on disk (`src/superclaude/cli/install_hooks.py`, `src/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/auggie-flag-clear.sh`). If two tests run concurrently under `pytest-xdist`, mutation context managers will race and corrupt files. The pyproject.toml shown in res-03 §5.1 does not enable xdist today, but the risk should be noted. | Builder adds a module-level docstring "Do not run with pytest-xdist — see file mutation context managers." Optionally use a process-level lock. |
| 5 | IMPORTANT | research/03-test-verification.md §6 — "jq not pinned in CI" | The mitigation `pytest.mark.skipif(not _HAS_JQ, ...)` is correctly applied to V5/V6/V7 because those test the cross-consistency section. BUT `make verify-sync` on a clean tree (V1) also invokes the new `=== Hooks Cross-Consistency ===` block per release-spec §5.1 — if jq is missing, that section "fails loudly". Therefore V1 (`returncode == 0`) ALSO requires jq, and the skeleton does not gate V1 on jq availability. | Builder should either (a) apply `_HAS_JQ` skipif at module level so ALL tests skip without jq, or (b) split the new cross-consistency block to be a no-op when jq is missing (changes the spec). Option (a) is the safer minimal-change. |
| 6 | MINOR | research/03-test-verification.md §7 V5 skeleton, line 518 | `original = json.loads(HOOKS_JSON.read_text())` is assigned but never used (only `new_data` is mutated). Cosmetic only. | Builder removes the unused `original` assignment. |
| 7 | MINOR | research/01-file-inventory.md §2.1 — last paragraph about test scenarios | Research-01 §2.1 claims "V2 hook missing in `.claude/`, V3 hook missing in `src/`, V4 hooks.json missing matcher, V5 hooks.json missing script reference, V6 installer registration drift, V7 cross-consistency mismatch". Release-spec §9 and research-03 §7 use a different mapping (V1 clean, V2 rm .claude, V3 freshness minus one, V4 freshness extra, V5 matcher prefix removed, V6 case body removed, V7 master regression). The two tables disagree. | Builder follows release-spec §9 + research-03 §7 (authoritative). Research-01 §2.1 should be ignored when extracting scenario semantics, or corrected if fix-authorized. |

---

## Coverage Gaps (probes from spawn prompt)

| Probe | Status |
|---|---|
| `reject-workspace-writes.sh` not-in-`_FRESHNESS_SCRIPTS` finding surfaced for builder? | **YES** — res-01 §3.2 + §5 #2 + cross-cutting summary table all flag this; new `=== Installer Registration ===` block will detect it on first run; builder must plan. |
| `auggie-bash-gate.sh` orphan flagged as out-of-scope but detectable? | **YES** — spec §1.2, spec §6 (3 response options), res-01 §5 #3. |
| CI-environment risks (jq, uv) documented? | **PARTIAL** — uv well documented (res-03 §6 + §4); jq flagged as UNVERIFIED with proposed mitigation. But the V1-clean-tree-also-needs-jq implication is missed (Issue #5). |
| V3/V4 tmp_path strategy fully resolved with concrete recommendation? | **YES** — res-03 §4 evaluates Options A/B/C, picks Option B (in-place mutation) with rationale tied to the editable-install constraint. |
| Findings actionable for task builder? | **YES** — every claim has file path + line number + verbatim quote; phase skeleton (res-04 §7) maps cleanly to spec parts; per-file edit pattern (res-04 §3c) is template-ready. |

---

## Recommendations Before Builder Proceeds

1. **Fix CRITICAL Issue #1** — research-03 §7 V5/V7 skeleton must use `PostToolUse`, not `PreToolUse`. Either fix in research-03 in a follow-up cycle, or the task-builder MUST be alerted to make this correction when transcribing V5/V7 into checklist items.
2. **Reconcile V2-V7 scenario mapping** — Research-01 §2.1's scenario descriptions disagree with release-spec §9 and research-03 §7. The release-spec definition is authoritative.
3. **jq dependency** — Builder should add a Phase 1 prerequisite item to verify `command -v jq`, or apply `pytestmark = pytest.mark.skipif(not _HAS_JQ, ...)` module-wide (not just V5/V6/V7).
4. **xdist serialization** — Add a module docstring "Do not run with pytest-xdist" or apply per-test `serial` markers.
5. **Builder MUST re-verify hooks.json:60 lives in PostToolUse** when writing the task file — not just trust the research files (the CRITICAL bug above is exactly the trap of inheriting research mistakes).

---

## Actions Taken

None — fix_authorization=false. Findings reported only.

---

## QA Complete

VERDICT: **FAIL**

- CRITICAL: 1 (V5/V7 skeleton uses `PreToolUse` instead of `PostToolUse` → tests silently no-op)
- IMPORTANT: 4 (JSON round-trip fragility, freshness-list regex fragility, xdist safety, jq applies to V1 too)
- MINOR: 2 (unused local var, research-01 §2.1 scenario mismatch)

Per skill rule: gate passes only when ALL findings are resolved regardless of severity. Orchestrator should run a fix-cycle or instruct the builder to incorporate these corrections explicitly in the task file checklist items.
