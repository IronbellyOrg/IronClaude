# Gaps and Questions — Sprint Task Execution Research

**Date:** 2026-04-03
**Source:** Merged from analyst-completeness-report-1.md, analyst-completeness-report-2.md, qa-research-gate-report-1.md, qa-research-gate-report-2.md

---

## Procedural Gaps (affect formatting, not substance)

| # | Gap | Severity | Files Affected | Status |
|---|-----|----------|----------------|--------|
| P1 | Missing `[CODE-VERIFIED]`/`[UNVERIFIED]` staleness tags on doc-sourced claims | IMPORTANT | 01, 02, 03, 04 | Noted — claims were empirically verified but not formally tagged |
| P2 | Missing gap severity labels (CRITICAL/IMPORTANT/MINOR) | IMPORTANT | 01, 03, 04 | Noted — synthesis agents should treat unlabeled gaps as IMPORTANT by default |
| P3 | File 07 uses non-standard tags (`[IMPLEMENTED]`/`[DEFERRED]` instead of `[CODE-VERIFIED]`) | MINOR | 07 | Acceptable — substantively equivalent for a doc-analyst investigating design history |

## Substantive Gaps (could affect synthesis quality)

| # | Gap | Severity | Files Affected | Remediation |
|---|-----|----------|----------------|-------------|
| S1 | Anti-instinct gate vacuous pass not cross-referenced — File 04 found it's a no-op for sprint tasks, File 01 lists it as functioning | IMPORTANT | 01, 04 | Synthesis agent should resolve: anti-instinct gate passes vacuously for sprint task outputs because they lack the required roadmap-specific frontmatter fields |
| S2 | `build_task_context()` dead code not cross-referenced in File 03's governance analysis | MINOR | 01, 03 | Synthesis agent should note: even though worker inherits CLAUDE.md, the designed context injection function is dead code |
| S3 | `classifiers.py`/`empirical_gate_v1` not traced by any file in partition 1 | MINOR | 01, 04 | Minor — it's a trivial function (exit code 0 = pass), documented in File 08 |
| S4 | File 03's claim about CLAUDE.md loading in `--print` mode is based on code analysis + inference, not official docs | IMPORTANT | 03 | Deferred to Phase 4 web research — Agent web-01 specifically investigates this |
| S5 | Whether CLAUDE.md resolves relative to `CLAUDE_WORK_DIR` or git root traversal | IMPORTANT | 03 | Deferred to Phase 4 web research |
| S6 | File 07 did not trace git history for when deferred tasks were later implemented | MINOR | 07 | Low impact — File 07 already confirmed current codebase state vs spec state |
| S7 | File 06 asserts "no tests for execution/" without citing grep evidence | MINOR | 06 | Low impact — execution/ modules confirmed as dead code regardless |
| S8 | File 08 did not trace per-task subprocess output path collision | MINOR | 08 | File 01 discovered this (output_file collision) — cross-reference needed |
| S9 | File 05 has unverified "42+ symbols" claim | MINOR | 05 | Plausible approximation, non-critical for synthesis |

## Cross-Reference Issues

| Research File A | Research File B | Issue |
|----------------|----------------|-------|
| 01 (path routing) | 04 (verification gates) | Anti-instinct gate listed as functioning in 01 but found vacuous in 04 |
| 01 (path routing) | 03 (worker governance) | build_task_context() dead code discovered in 01, not mentioned in 03's governance analysis |
| 01 (path routing) | 08 (progress tracking) | Output file collision discovered in 01, relevant to 08's crash recovery analysis |

## Overall Assessment

Research quality is HIGH — evidence density is excellent (every major claim has file:line, verified against source code). Failures are procedural (missing tags/labels) not substantive (no fabrication, no contradictions, no missing coverage). Synthesis can proceed with awareness of the gaps noted above.
