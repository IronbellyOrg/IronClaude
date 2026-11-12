# Diff Analysis: reflect post-execution reviewer cards (3 variants)

## Metadata
- Generated: 2026-11-12 (reflect-post-20261112T192600Z-TASK-RF-sweep-phase1)
- Variants compared: 3 (V1 reviewer 1 analyzer/sonnet, V2 reviewer 2 qa/haiku, V3 reviewer 3 refactorer/opus), each with its blind calibration attached
- Focus: correctness, coverage, deviation-classification
- Total differences found: structural 3, content 18, contradictions 5, unique 6, shared assumptions 4
- Categories: structural (3), content (18), contradictions (5), unique (6), shared assumptions (4)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card sections | lead_verdicts, findings, grounding_gaps, inferred_claims | adds `objective_checks` (7 task objectives) | adds `checked_clean` list | Low |
| S-002 | Severity scale in use | minor/medium | minor/medium/blocking (3 blocking) | minor/medium (none blocking) | High (drives the verdict) |
| S-003 | Class vocabulary | authorized, necessary, drift | authorized, necessary, drift, regression | authorized, drift, regression | Medium |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Rule 5 `working` inert / FR-006 | R1-F1 authorized minor; R1-F2 necessary minor (agent-wait feed) | R2-F6 regression blocking (cites owner approval as authorization_source) | not examined | High |
| C-002 | Ledger over 1 MiB read tail only (SPEC :295, DESIGN :62) | not flagged | R2-F5 regression blocking | R3-F4 regression medium | Medium |
| C-003 | `subprocess.run` instead of Popen + kill at 8 MiB (SPEC :286) | R1-F4 drift medium | not examined | R3-F3 regression medium | Medium |
| C-004 | Worker-list row without valid dispatchId dropped and invisible to FR-010 origin guard | R1-F3 drift medium | not examined | not examined | Medium |
| C-005 | `_git` over-limit reason `bytes` vs SPEC `8 MiB` | R1-F5 drift minor | not examined | mentioned inside R3-F3 | Low |
| C-006 | `core.fsmonitor` can run in scanned worktrees | not examined | not examined | R3-F1 drift medium | Medium |
| C-007 | Disk readers do not check for a regular file (FIFO) | not examined | not examined | R3-F2 drift medium | Medium |
| C-008 | Third per-Run source row and extra model fields beyond DESIGN 7.2/7.4 | R1-F6 drift minor; R1-F7 authorized minor | not examined | R3-F8 drift minor | Low |
| C-009 | Stale DESIGN banner and task Open Questions (OQ-2..OQ-8 PENDING) | not examined | R2-F1 drift medium | not examined | Medium |
| C-010 | FIN-F7 limitation (exempt reply omits outage) | not examined | R2-F2 authorized medium | not examined | Low |
| C-011 | Full pytest / format check not green | not examined | R2-F3 necessary medium | not examined | Low |
| C-012 | NFR-007 "still publish" tests stop at `report.render` | not examined | R2-F4 regression blocking | not examined | Medium |
| C-013 | HOW-WE-WORK "on every wake" vs WC-16 "wake or wait timeout" | not examined | not examined | R3-F10 authorized minor | Low |
| C-014 | pragmatic.md sweep chat-summary exception | not examined | not examined | R3-F9 authorized minor | Low |
| C-015 | JSON `report_path` passes through the Markdown sanitizer | not examined | not examined | R3-F5 drift medium | Medium |
| C-016 | SKILL step 5 says "the standard error line" (one line) | not examined | not examined | R3-F6 drift minor | Low |
| C-017 | XDG state folder computed twice; wrappers with test-only callers | not examined | not examined | R3-F7 drift minor | Low |
| C-018 | `total_is_lower_bound` always True | R1-F8 necessary minor | not examined | not examined | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Class of the Rule 5 / FR-006 gap | authorized (owner decision) | regression, blocking, while naming the owner decision as its own authorization_source | n/a | High |
| X-002 | Class and severity of the ledger tail-only read | not flagged | regression blocking | regression medium (practical risk "low") | Medium |
| X-003 | Class of the Popen-vs-run departure | drift medium | n/a | regression medium | Medium |
| X-004 | Whether the R2 "every wake" wording is authorized or a drift | n/a | n/a | authorized (DESIGN :717 copied verbatim) vs T1 lead necessary | Low |
| X-005 | Is a test-only gap (NFR-007) a regression | n/a | regression blocking | n/a (calibrator: drift medium) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | The FR-010 origin-guard hole for dropped worker-list rows, traced to `classify.py:690-694` and the empty-rows case | High |
| U-002 | V2 | Seven-objective check against disk and the claim-test mismatch for NFR-007 (`test_probes_allowlist.py:1144`, `:1169`) | High |
| U-003 | V2 | Stale approval text in DESIGN :5 and task Open Questions OQ-2..OQ-8 | Medium |
| U-004 | V3 | fsmonitor and FIFO hardening gaps, sanitize of `report_path` | High |
| U-005 | V3 | `checked_clean` list (no `src/superclaude/` path in primitives, never-as-worker, `.gitignore`) | Medium |
| U-006 | V1 | `total_is_lower_bound` inline shortcut and `_git` reason wording pinned by a test | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | DESIGN text overrides SPEC text wherever they differ (so code that matches DESIGN is not a Regression against SPEC) | all variants (R1-F1, R2-F6 authorization, R3-F4) | High: decides Regression vs Drift/Authorized for C-001, C-002, C-003 | UNSTATED for unlisted differences (DESIGN 15.2 says DESIGN wins over REPORT only; section 13 lists SPEC deviations) - promoted |
| A-002 | A Regression needs a behaviour change that breaks an acceptance criterion; a test-only or wording gap is Drift | V1, calibrators | High | UNSTATED - promoted |
| A-003 | The audited tree equals the diff (no later edits) | all | Low: regenerated diff is byte-identical (orchestrator check) | STATED in the T1 card |
| A-004 | Tasklist plan items are authority only for the task, never for the SPEC or DESIGN | V3 (R3-F3 authorization_source note) | Medium | UNSTATED - promoted |

## Summary
- Total structural differences: 3
- Total content differences: 18
- Total contradictions: 5
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: S-002, C-001, X-001, A-001, A-002
