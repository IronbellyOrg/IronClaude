---
protocol: sc-reflect
use_case: UC-1
tier: T1
phase: 7
milestone: M7
title: "Observability, TUI, Detached & Full CLI Surface"
tasklist: ../phase-7-tasklist.md
spec: ../../roadmap.md (## M7 section)
generated: 2026-06-01
mode: single-agent grounded pass
verdict: PASS_WITH_NOTES
coverage_pct: 100
fidelity_score: 0.95
tier_calibration: APPROPRIATE
m7_spec_items: 17
phase_tasks: 17
phase_checkpoints: 4
---

# sc-reflect UC-1 T1 — Phase 7 Validation Report

## §1. Coverage Matrix (M7 spec → Phase-7 tasks)

| # | M7 ID | Title | Mapped Task | Status |
|---|-------|-------|-------------|--------|
| 1 | COMP-013 | tui (Rich Live, flag-gated) | T07.01 | COVERED |
| 2 | COMP-014 | tmux detached wrapper | T07.02 | COVERED |
| 3 | INV-012 | TUI opt-in via --tui | T07.03 | COVERED (STRICT) |
| 4 | FR-002 | swarm status subcommand | T07.04 | COVERED |
| 5 | FR-003 | swarm logs subcommand | T07.05 | COVERED |
| 6 | FR-004 | swarm attach subcommand | T07.07 | COVERED |
| 7 | FR-005 | swarm kill subcommand | T07.08 | COVERED |
| 8 | FR-006 | swarm scaffold subcommand | T07.09 | COVERED |
| 9 | FR-013 | Three monitoring patterns | T07.10 | COVERED |
| 10 | FR-014 | Detached mode via tmux (--detached) | T07.11 | COVERED |
| 11 | FR-027 | Done sentinel emission (done.json) | T07.13 | COVERED (STRICT) |
| 12 | NFR-004 | Three-layer durable monitoring | T07.14 | COVERED |
| 13 | NFR-016 | Contract surface non-precluding | T07.15 | COVERED (STRICT) |
| 14 | AC-007 | Rich ≥13.0.0 for --tui | T07.16 | COVERED |
| 15 | AC-008 | tmux required for detached | T07.17 | COVERED |
| 16 | AC-009 | No external framework integration | T07.19 | COVERED |
| 17 | AC-016 | No streaming/function-calling/vision | T07.20 | COVERED |

**Coverage: 17/17 spec items = 100%.** Four checkpoints (T07.06, T07.12, T07.18, T07.21) gate the phase at logical seams (after 5 tasks, after 11 tasks, after 17 tasks, end-of-phase). All checkpoints carry Tier=EXEMPT (correct per protocol — gates are not work-items).

## §2. Fidelity Findings

### F1 — Eight-subcommand exit criterion preserved
Roadmap M7 exit: "all 8 subcommands functional." Phase-7 checkpoint T07.12 explicitly asserts: "Eight subcommands present: run/status/logs/attach/kill/scaffold/validate/validate-lenses" and validates via `swarm --help`. **Fidelity: exact.**

### F2 — INV-012 non-TTY guarantee preserved
Spec: "non-TTY callers do not get terminal control sequences." T07.03 acceptance includes "Non-TTY caller never receives terminal control sequences" with validation `swarm run --transport stub | cat` producing no ANSI escapes (verified by grep on captured stdout). **Fidelity: exact + testable.**

### F3 — Three monitoring patterns enumerated
Spec FR-013 lists three patterns: `Bash run_in_background + until [ -f done.json ]`, `Monitor` tailing JSONL, `swarm status --watch`. T07.10 step 1 enumerates the same three verbatim. **Fidelity: exact.**

### F4 — Three-layer durable monitoring (NFR-004) — minor naming note
Spec says "three-layer durable monitoring" but enumerates **four** artifacts: `.swarm-state.json` + `execution-log.jsonl` + `execution-log.md` + `done.json`. Phase goal statement and T07.14 both call this out as "three-layer ... 4 artifacts" — internally consistent with the roadmap's own naming. **Fidelity: preserves the roadmap's terminology including its slight tension; not a divergence.**

### F5 — Done sentinel atomic-write preserved
Spec FR-027: "atomic write." T07.13 step 2 specifies "tmp+`os.replace`" and AC requires "Terminal state writes `done.json` atomically." Cross-reference to DM-017 (atomic_write:bool(true)) preserved. **Fidelity: exact.**

### F6 — Detached survival semantic preserved
Spec NFR-016: "detached mode guarantees caller-death survival." T07.11 AC: "Detached job survives caller exit (verified by subprocess kill of parent)." T07.15 AC adds: "Detached job survives caller kill (verified via subprocess SIGKILL)." **Fidelity: exact, redundantly enforced.**

### F7 — Grep-audit pattern coverage
T07.15 enumerates forbidden patterns: `Read`, `Edit`, `Bash`, `claude.ai`, `anthropic`, `Tool`. Spec NFR-016 / AC-013 says "zero Claude tool names." Patterns cover the canonical Claude tool surface. **Fidelity: appropriate; may be conservative (also catches generic "Tool" but that's intentional belt-and-suspenders).**

### F8 — All M7 IDs trace 1:1
Every R-118..R-134 roadmap ID maps to exactly one T07.NN task. No orphan tasks; no orphan spec items.

## §3. Best-Practice / Anti-Pattern Findings

### BP1 — Tier calibration is appropriate (special-note concern resolved)
The user flagged: "M7 is largely STANDARD tier ... verify tier classification doesn't over-strict." Reviewed:

- **STRICT (3):** T07.03 (INV-012), T07.13 (FR-027 done sentinel), T07.15 (NFR-016 contract-surface audit). Each carries `Critical Path Override: YES`. All three are non-Python-caller compatibility guards — silent failure here breaks the entire NFR-016 caller-agnostic premise.
- **LIGHT (3):** T07.16 (Rich pin), T07.17 (tmux fallback doc), T07.20 (transport-limits doc). Doc/dependency tasks correctly LIGHT.
- **STANDARD (11):** TUI module, tmux module, status/logs/attach/kill/scaffold subcommands, detached mode, monitoring patterns, three-layer artifact verification, AC-009 framework audit.

**Verdict: No over-stricting.** Only the genuinely caller-facing guarantees (non-TTY purity, done-sentinel atomicity, Claude-ism leakage) carry STRICT. AC-009 (T07.19) is STANDARD rather than STRICT, which is a defensible call — no Claude-tool leakage path, but a future-proofing audit.

### BP2 — Checkpoint placement is well-spaced
Mid-phase gates at task 5 (CP1), task 11 (CP2), task 17 (CP3 — invariants), and end-of-phase (CP4). This bounds the blast radius of regressions to ~5-task windows. Phase-7 has 21 total items including 4 checkpoints — average 5.25 tasks per gate, consistent with sprint best practice.

### BP3 — Dependencies are explicit and acyclic
T07.07 (attach) and T07.08 (kill) correctly depend on T07.02 (tmux). T07.03 (INV-012) correctly depends on T07.01 (TUI module). T07.11 (detached) depends on T07.02. T07.10 (monitoring patterns) depends on T07.04 + T07.13. **No cycles.** All inter-task and cross-phase (T03.01, T03.03, T03.04, T02.14, T02.28, T05.01, T01.10) dependencies cite real upstream task IDs.

### BP4 — Each task has Verification + Acceptance + Validation triad
Every T07.NN provides: explicit `Verification` field (tests file), AC list, and `Validation` block with runnable commands. No "TODO" stubs. Pattern matches sprint discipline.

### BP5 — Rollback fields appropriate
Most tasks have meaningful rollback (disable flag, remove subcommand, unpin). Three guard-type tasks (T07.03, T07.13, T07.14, T07.15, T07.17) correctly say "Rollback: none — guard/observability guard/caller-agnostic guard." Aligns with their STRICT/critical-path nature.

### AP1 — Minor: T07.06 mid-phase checkpoint validation runs Phase-7 tests but does not gate on tier T07.03 STRICT failure
Mostly cosmetic — the checkpoint's pytest invocation includes test_inv012_tui_opt_in.py, so a STRICT failure does block CP1. No real anti-pattern.

### AP2 — Minor: AC field substring rule not separately re-validated
NFR-012 / §11.5 substring is M2's concern (T07.NN doesn't re-validate). This is correct scope — M7 is operator surface, not preflight — but a reader could misread the grep audit (T07.15) as covering injection-guard. The two are distinct. Not a fidelity bug, but worth noting if M7 review reviewers conflate them.

## §4. Deviation Taxonomy

| Category | Count | Notes |
|---|---|---|
| Authorized expansion | 0 | No phase-only additions beyond M7 spec |
| Necessary deviation | 0 | None identified |
| Drift | 0 | No silent scope reduction or expansion |
| Regression | 0 | No fidelity loss vs. roadmap |

**Net: Zero deviations.** Phase-7 tasklist is a faithful expansion of M7.

## §5. Calibration

- **Heterogeneous review:** N/A at T1 (single-agent). T2 escalation not triggered.
- **Blind calibration:** N/A at T1.
- **Evidence-validator gate:** Every Phase-7 task cites a roadmap R-NNN id traceable to M7 row; every acceptance criterion has a runnable `Validation` command; every dependency resolves to a real upstream task. **Gate: PASS.**

## §6. Evidence Summary

| Claim | Evidence (file:line range) |
|---|---|
| 17/17 M7 spec items covered | roadmap.md §M7 table rows 1-17 (lines 397-414) ↔ phase-7-tasklist.md T07.01..T07.20 minus checkpoints |
| Tier=STRICT only for caller-facing guards | phase-7-tasklist.md lines 85-89, 410-411, 481 (Critical Path Override:YES) |
| Eight-subcommand assertion preserved | phase-7-tasklist.md line 393; roadmap.md line 394 |
| Three monitoring patterns enumerated identically | phase-7-tasklist.md line 328; roadmap.md FR-013 (line 406) |
| Atomic-write done sentinel | phase-7-tasklist.md line 421 ("tmp+`os.replace`"); roadmap.md FR-027 (line 408) + DM-017 (line 104) |
| Detached survives caller kill | phase-7-tasklist.md line 372, 498; roadmap.md NFR-016 (line 410) |
| Forbidden grep patterns canonical | phase-7-tasklist.md line 491 (Read/Edit/Bash/claude.ai/anthropic/Tool) |
| Phase-7 has 17 tasks + 4 checkpoints | phase-7-tasklist.md T07.01..T07.21 |

## §7. Recommendations

1. **(Optional, cosmetic)** In T07.10 doc, explicitly note that "three-layer durable monitoring" refers to the three monitoring *patterns* (FR-013), and "four artifacts" refers to NFR-004's emission set. This pre-empts reader confusion about the roadmap's 3-vs-4 numbering tension. No code change needed.
2. **(Optional)** Consider adding a one-line note in T07.15 clarifying that the grep audit covers caller-isms only, distinct from the §11.5 injection-guard substring check (M2 scope). Reduces reviewer confusion at PR time.
3. **(No action required)** Tier calibration is correct as-is. The three STRICT/Critical-Path overrides (T07.03, T07.13, T07.15) are well-justified by their caller-agnosticism role; do not downgrade.

---

## VERDICT

**PASS_WITH_NOTES** — Phase-7 tasklist is a faithful, complete expansion of roadmap M7. Coverage is 100% (17/17 spec items). Tier calibration is appropriate (3 STRICT, 3 LIGHT, 11 STANDARD, 4 EXEMPT checkpoints). Zero deviations under the 4-category taxonomy. Evidence-validator gate passes. Recommendations §7.1 and §7.2 are cosmetic; no remediation required to proceed to execution.

**T2 escalation:** NOT required.
**T3 remediation:** NOT required.
**Proceed:** Phase-7 tasklist is execution-ready.
