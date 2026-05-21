# cliEval P4/P5 Runner-Symbol Investigation — Final Summary

**Pipeline**: `/sc:spawn` → 4× Phase-1A agents (analyze + 3× troubleshoot) → adversarial debate → 4× Phase-2A agents (2× brainstorm + 2× design) → adversarial red-team → final tasklist
**Duration**: ~6 minutes wall-clock, ~1.2M tokens across 10 sub-agents
**Workspace**: `.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/`

---

## Problem statement

`src/superclaude/cli/eval/commands.py:eval_run` (lines 1406–1695) references 11 module-level symbols that are never defined. Ruff reports 11 F821 + 12 F401. `superclaude eval run --help` works (decorator stack parses), but any actual invocation raises `NameError`. This blocks both Phase-4 and Phase-5 sprint exit gates (`CP-P04-END.md` and `CP-P05-END.md` both `status: FAIL`).

## Root cause — HYBRID T1+T3 (Phase 1B verdict, confidence 0.86)

The entire `src/superclaude/cli/eval/` tree is **untracked in git** (`git ls-files` returns 0 rows; `git status` reports `?? src/superclaude/cli/eval/`). The 11 "missing symbols" were never authored, never committed, never removed — the working tree contains a body written by one sprint sub-agent against helpers that another sprint sub-agent was supposed to write but never did. Per-symbol breakdown:

| Bucket | Count | Symbols |
|---|---|---|
| Net-new (T1): author locally in commands.py | 7 | `_utc_iso_now`, `_can_install_signal_handler`, `_compute_run_stats`, `_format_run_summary_line`, `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`, `RUN_INTERRUPTED_EXIT_CODE` |
| Sibling-wrapper (T3): thin glue over already-landed sibling helpers | 4 | `_new_run_id` → `compose_run_id`; `_default_output_dir` → `compose_run_dir`; `_resolve_executor_factory` → `type[LifecycleExecutor]`; `_run_one_spec` → `EvalRunner.run` + `allocate_per_eval_paths` + `HomeIsolation` |

Decisive evidence: 5 test modules (`test_no_mcp_skip.py`, `test_single_command.py`, `test_exit_codes.py`, `test_no_pty_exclusion.py`, `test_retention_policy.py`) already enumerate the missing symbols by name and skip-gate themselves with docstrings calling these "T04.10 deliverables… not yet landed" — the defect is **documented as a known forward dependency**. Project narrative uses "author" / "wires" / "adds" verbs for these symbols (CP-P04-END.md:109, D-0081/notes.md:106). Never-authored.

## Refinements forced by red-team (Phase 2B, 12 attacks, 3 CONFIRMED)

1. **ATK-1 — Call-site reorder is internally inconsistent.** D1's plan to move `_new_run_id` from line 1467 to line 1530.5 would orphan lines 1482–1499 (`home_root.mkdir`, `runtime_config`) which depend on `resolved_output`. **Refactor**: keep call sites at 1467/1469; use 2-arg wrappers `_new_run_id(started_iso, suite)` and `_default_output_dir(started_iso, suite)`; hoist only `started_iso = _utc_iso_now()` to line 1466.
2. **ATK-8 — Hardcoded n_prime invariant.** `_compute_run_stats` cannot statically set `kept_plus_skipped_equals_n_prime=True` — `RunSummary.__post_init__` at models.py:896-912 asserts it. **Refactor**: compute `(kept_k + skipped_s == expanded_n_prime)` at runtime.
3. **ATK-11 — Executor-factory shape underspecified.** `ClaudeProcessAdapter.__init__` requires per-eval kwargs unavailable at factory-construction time. **Refactor**: factory returns `type[LifecycleExecutor]` (the constructor); `_run_one_spec` invokes with full kwargs. Add `ExecutorFactory = type[LifecycleExecutor]` type alias.

Most surprising finding from red-team: `secrets` import currently F401 but **must stay** because `_run_one_spec` uses `secrets.token_hex(8)` for the run-id salt — the F401 cleanup is "11 → 0 via consumption + 1 → 0 via deletion of `import os`", not "12 → 0 via deletion" as D1 originally claimed.

## Final budget

- **+139 LOC** across 3 files (commands.py +94 / −4, test_eval_run.py +45 NEW, test_eval_group.py 1-line edit)
- **17 atomic tasks** in linear dependency chain; T13a triage + T14-1/T14-2 verification gates
- All atomic tasks ≤30 LOC

## Carry-forward (NOT blockers for sprint exit)

- D-0070/D-0071/D-0072/D-0077 artifact-triplet authoring (Phase-4 doc gap)
- OQ-2 sign-off in decisions.md:577 (requires RyanW; Phase-5 carry-forward)
- C2/C6 sibling-promotion refactor (v2 cleanup — promote `_compute_run_stats` to `RunCounts.from_outcomes` classmethod)

## Deliverable inventory

| File | Lines | Role |
|---|---|---|
| `phase1/A1-module-audit.md` | – | Structural audit + 11-row semantic-equivalence map |
| `phase1/A2-thesis-never-authored.md` | – | T1 defense (confidence 0.82) |
| `phase1/A3-thesis-removed.md` | – | T2 honestly self-refuted (confidence 0.03) |
| `phase1/A4-thesis-belong-elsewhere.md` | – | T3 defense (confidence 0.30) |
| `phase1/A[1-4]-branch-trace.md` | – | Rule 2.5 trace artifacts (19 expected lines each) |
| `phase1B-debate-verdict.md` | – | 3-round adversarial synthesis + 11-row verdict |
| `phase2/B1-solution-space.md` | – | 6 candidates + churn×fidelity×risk grid |
| `phase2/B2-anti-patterns-and-fringe.md` | – | 8 anti-patterns + 7 fringe approaches |
| `phase2/D1-design-primary.md` | 486 | C1 Minimal in-place — full implementation spec |
| `phase2/D2-design-alternative.md` | – | C2 Lifted aggregator — alternative + §10 comparison |
| `phase2B-final-design.md` | 196 | Red-team attack matrix + refactored D1-final |
| `REMEDIATION-TASKLIST.md` | 524 | 17 atomic tasks, ready for /sc:task execution |
| `artifacts/expected-branches-extended.txt` | 20 | Authoritative branch-line baseline for Rule 2.5 gate |

## Hand-off

Execute the remediation tasklist via STRICT-tier task pipeline:

`/sc:task .dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/REMEDIATION-TASKLIST.md --strategy systematic --compliance strict`
