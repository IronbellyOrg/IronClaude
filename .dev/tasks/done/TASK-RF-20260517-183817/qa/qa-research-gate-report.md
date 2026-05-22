# QA Report — Research Gate

**Topic:** hook-sync-and-matcher-fix release task-builder research verification
**Date:** 2026-05-17
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

**Critical finding:** R1's summary contains an internal contradiction that, if propagated to the builder, would cause Part 2 of the release to be omitted from the task file. R1 verified the BUGGY current state of `hooks.json:60` and `auggie-flag-clear.sh:22` correctly, then misinterpreted that buggy state as "already at target state." The release-spec §4.1/§4.2 unambiguously shows both files require a `mcp__auggie-mcp__` addition (confirmed missing from both by independent grep).

Builder MUST be re-briefed that Part 2 is a real two-line patch, not a no-op, before the task file is built.

---

## Confidence

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep/Bash-grep: 6 | Glob/ls: 4 | Bash: 5

Every check below has a cited tool invocation against the source file, not against R1-R4's claims.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — all 4 research files have Status: Complete + Summary | PASS | `ls -la` shows all 4 files present (12961, 26716, 18750, 23494 bytes). Each opened with `Status: Complete` near top; each ends with a "Summary"/"Final recommendation"/"Summary for the builder" section. |
| 2 | Evidence density — every [CODE-VERIFIED] claim in R1 actually checked | PASS-on-evidence / FAIL-on-interpretation | hooks.json:60 reads exactly `"mcp__auggie__.*\|mcp__airis-mcp-gateway__auggie_.*"` (verified by Read). auggie-flag-clear.sh:22 reads exactly `mcp__auggie__*\|mcp__airis-mcp-gateway__auggie_*)` (verified). Makefile:154-247 has no `=== Hooks ===` (verified, banners at L158/L190/L216 only). install_hooks.py:43 declares `_FRESHNESS_SCRIPTS` (verified), iteration at L178 confirmed (`grep -n "for name in _FRESHNESS_SCRIPTS"` returned `178:`). `.claude/hooks/auggie-bash-gate.sh` exists (2593 bytes, mtime May 17 17:58); `src/superclaude/hooks/scripts/auggie-bash-gate.sh` does NOT exist (verified by `ls`). BUT see Finding C1 — R1's interpretive summary is wrong. |
| 3 | Scope coverage — every key file/dir examined | PASS | research-notes.md EXISTING_FILES lists hooks.json, auggie-flag-clear.sh, Makefile, install_hooks.py, tests/, MDTM template. R1 covers files 1-4; R2 covers Makefile; R3 covers test harness; R4 covers template. All present. |
| 4 | Documentation cross-validation — doc-sourced claims tagged | PASS | All R1 claims tagged `[CODE-VERIFIED]` with a file:line. R2-R4 either cite source files directly or quote the spec. No untagged doc claims. |
| 5 | Contradiction resolution — no unresolved conflicts | FAIL | **Finding C1.** R1 §"Summary of [CODE-VERIFIED] Claims" rows 1-2 say "Already at target state". R1 §"Additional findings" bullet 1 says "Spec claims 1 + 2 are ALREADY satisfied at HEAD" and "Part 1 diff would be a no-op". This contradicts release-spec.md §4.1/§4.2 which shows explicit diffs adding `mcp__auggie-mcp__.*` (regex) and `mcp__auggie-mcp__*` (glob) to BOTH files. Independent verification by `grep -c "mcp__auggie-mcp__" src/superclaude/hooks/hooks.json` returned 0; grep across `src/superclaude/hooks/` returned 0 hits. R1 confused the existing `airis-mcp-gateway__auggie_` alternative (present) with the missing `mcp__auggie-mcp__` alternative (absent). Note R1's "Spec Claim 1" mis-labels the spec — release-spec §4.1 is a PATCH spec, not a "current state" claim. |
| 6 | Gap severity classification — CRITICAL items flagged | PASS | R2 §4.3 D4 flags `<(...)` process-substitution as **CRITICAL** with explicit POSIX/dash failure mode. R3 §2 flags the `tmp_path + _FRESHNESS_SCRIPTS` mutation gap and supplies an empirically-verified PYTHONPATH solution. Both critical issues are surfaced. |
| 7 | Depth appropriateness — matches Standard tier | PASS | 4 files, ~80KB total. R1 covers 6 spec claims with line-by-line citations. R2 catalogs 11 divergences (D1-D11). R3 covers V1-V7 scenarios with empirical command output. R4 maps 13 template sections and 2 example tasks. This is full Standard tier coverage. |
| 8 | Integration point coverage — Makefile ↔ Python ↔ shell ↔ JSON ↔ pytest | PASS | R2 §3 table catalogs every tool the new sections add (`jq`, `comm`, `xargs`, `sort`, `uv run`, `grep -oE`). R3 §2 covers Python↔Make boundary via `uv run python -c`. R3 §8 covers Makefile↔pytest via subprocess.run. Cross-section coverage is explicit. |
| 9 | Pattern documentation — code patterns captured | PASS | R2 §2 catalogs 10 pattern elements with verbatim quotes (section headers, drift accumulator, forward/reverse loop shapes, diff variants, skip patterns, status symbols, indent rules, shell continuation). R3 §1a-1d catalogs subprocess+tmp_path+PYTHONPATH pattern. R4 §1-2 catalogs 13 template sections. |
| 10 | Incremental writing compliance — files show iterative structure | PASS | All 4 files have section-by-section growth with numbered sub-headers (1.1, 1.2, 2.1...). Sizes correlate with depth (R2 = 26716 bytes is largest, matches the most pattern detail). No one-shotted artifacts (verbose verbatim code blocks, hand-written D1-D11 divergences). Mtimes are spread across May 17 18:54-18:58 (incremental). |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| C1 | CRITICAL | `research/01-surface-verification.md` §"Summary of [CODE-VERIFIED] Claims" rows 1-2 + §"Additional findings" bullet 1 | R1 calls the buggy current state of `hooks.json:60` and `auggie-flag-clear.sh:22` "Already at target state" and writes that "Spec claims 1 + 2 are ALREADY satisfied at HEAD" → "Part 1 diff would be a no-op against current master." This is FALSE per release-spec §4.1/§4.2 which explicitly diffs in `\|mcp__auggie-mcp__.*` (hooks.json:60) and `\|mcp__auggie-mcp__*` (auggie-flag-clear.sh:22). Independent grep confirms `mcp__auggie-mcp__` is NOT present in either source file (0 matches). If the builder reads R1's summary as the operational truth, Part 2 of the release will be silently dropped from the task file. R1's research-level facts are correct (the quoted line content matches the source); R1's INTERPRETATION of those facts versus the spec is inverted. | R1 must be re-issued with a corrected summary stating: "Part 2 patches are REQUIRED — current `hooks.json:60` and `auggie-flag-clear.sh:22` both lack `mcp__auggie-mcp__` and must be widened per release-spec §4.1/§4.2." Recommend prepending an explicit "Bug A confirmed present" callout at the top of R1. Alternative: if R1 is left as-is, the builder spawn prompt MUST include an override note: "R1's summary mislabels Part 2 as no-op — Part 2 is a real 2-line patch; verify against release-spec §4.1/§4.2." |
| M1 | MINOR | `research/01-surface-verification.md` §"Spec Claim 3" | R1 verifies the *current* `auggie-flag-clear.sh:2` header comment but does not flag that release-spec §4.2 also requires this line to be REWRITTEN to enumerate all 3 prefixes. R1's summary table omits this from the patch list. | Add a row to R1's summary noting that line 2's comment is also part of the Part 2 diff (per spec §4.2, lines 159-163). |
| M2 | MINOR | `research/02-makefile-patterns.md` §5.2 + §4.3 D4 | R2 correctly flags `<(...)` as bash-only and recommends `SHELL := /bin/bash`. Independent check: `grep -nE "^SHELL\|^\.SHELLFLAGS" Makefile` returns no matches — the Makefile has NO `SHELL` declaration. On Debian/Ubuntu where `/bin/sh → dash`, the spec's process-substitution will fail. R2's recommendation is correct but the builder needs this surfaced as a MUST-DO at task-file time, not just embedded in §5.2's "CRITICAL BUILDER NOTE". | Either elevate to a top-of-R2 callout, OR ensure the builder's task file has an explicit Phase-1 item: "Add `SHELL := /bin/bash` to Makefile head OR rewrite §5.2 with temp files". |

---

## Adversarial cross-checks performed (independent of R1-R4)

| Spec claim under scrutiny | Independent verification | Result |
|---|---|---|
| hooks.json:60 missing `mcp__auggie-mcp__` (release-spec §4.1 diff) | `grep -c "mcp__auggie-mcp__" src/superclaude/hooks/hooks.json` → 0; `grep -rn "mcp__auggie-mcp__" src/superclaude/hooks/` → 0 hits | **CONFIRMED MISSING** — R1's summary is wrong; Bug A is real |
| auggie-flag-clear.sh:22 missing `mcp__auggie-mcp__` (release-spec §4.2 diff) | grep above also covers this file; 0 hits | **CONFIRMED MISSING** |
| Makefile has no `SHELL := /bin/bash` declaration (R2 D4 concern) | `grep -nE "^SHELL\|^\.SHELLFLAGS" Makefile` → 0 matches | **CONFIRMED ABSENT** — D4 risk is real |
| Makefile drift accumulator scope ends at line 240 (R2 §6 insertion claim) | Read Makefile:240-247 directly — line 240 closes the Commands reverse loop with `done; \`; line 241 is `echo ""; \`; lines 242-246 are the final `if [ "$$drift" -eq 0 ]` block | **CONFIRMED** — new sections must insert between 240 and 241 |
| install_hooks.py uses `uv run python -c` pattern (R3 §2 PYTHONPATH claim) | Spec snippet at hook-sync-coverage-spec.md:96 reads `registered=$$(uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print('\\n'.join(sorted(_FRESHNESS_SCRIPTS)))" 2>/dev/null)` — confirmed; R3's PYTHONPATH logic applies | **CONFIRMED** — `uv run` inherits parent PYTHONPATH; R3's empirical test pattern is sound |
| R3 PYTHONPATH override would import tmp_path/src first | Logic check: when subprocess.run sets `env={**os.environ, "PYTHONPATH": str(tmp_path / "src") + os.pathsep + existing}`, `uv run`'s subprocess inherits this env. Python's `sys.path` is constructed from PYTHONPATH first, then site-packages. The editable install's `.pth` entry in site-packages is AFTER PYTHONPATH. tmp_path/src DOES win. | **CONFIRMED** — R3's reasoning is correct |
| 27-37 items proportionate for ~155 LOC of changes (R4 §6 claim) | TASK-RF-track-2 (closest analog cited by R4) has ~16 items for a much smaller mechanical change. TASK-RF-track-3 has ~33 items for 47 files/79 renames. R4's range bridges these: 27 items for the smaller side (3 file patches + 3 Makefile sections + 1 test file ≈ ~7 core edits + Phase 1 setup + gates + Post-Completion = ~20-27); 37 items for the verbose side (split test file into L1+L2; per-AC verification items). | **PROPORTIONATE** — R4's recommendation is well-calibrated |
| `.claude/hooks/auggie-bash-gate.sh` has no `_FRESHNESS_SCRIPTS` or hooks.json registration | `grep -c "auggie-bash-gate.sh" src/superclaude/hooks/hooks.json` → 0 | **CONFIRMED** — orphan is unregistered everywhere, consistent with R1's claim |

All adversarial cross-checks except C1 confirm the research. The single critical defect is R1's interpretive summary, not its verified facts.

---

## Summary

- Checks passed: 9 / 10
- Checks failed: 1 (Contradiction resolution — Finding C1)
- Critical issues: 1
- Important issues: 0
- Minor issues: 2
- Issues fixed in-place: 0 (fix_authorization: false)

The research files contain *more than enough verified evidence* to build a correct task file. The defect is a single interpretive error in R1's summary that contradicts both the spec and R1's own quoted file content. If the builder reads R1's checkboxes literally rather than R1's narrative summary, the task file will be correct. If the builder trusts R1's narrative summary, Part 2 of the release will be omitted.

---

## Recommendations

1. **MUST FIX before builder is spawned (CRITICAL):** Re-issue R1 with a corrected summary that frames `mcp__auggie-mcp__` as MISSING from both files, and explicitly marks Bug A (release-spec §1.1) as CONFIRMED PRESENT. OR include an override clause in the builder's spawn prompt that points to release-spec §4.1/§4.2 as the authoritative diff source and warns against R1's summary interpretation.
2. **MUST FIX before builder is spawned:** Surface the Makefile `SHELL :=` gap (Minor M2) as a builder-action in Phase 1: "Verify or add `SHELL := /bin/bash` to Makefile head before pasting Installer Registration block, OR substitute the temp-file variant from R2 §5.2 alternative."
3. **SHOULD FIX:** Add the line-2 header-comment update to R1's summary table (Minor M1) so the builder doesn't omit it from the Part 2 patch.
4. Once the above are resolved, the research foundation is sufficient for a Standard-tier task file build.

## QA Complete

**Verdict: FAIL** — Critical contradiction in R1's summary must be resolved before builder is spawned. Two minor issues are nice-to-fix but would not by themselves block the build if the spec is treated as the authoritative reference. ALL three findings must be resolved per zero-tolerance gate semantics.
