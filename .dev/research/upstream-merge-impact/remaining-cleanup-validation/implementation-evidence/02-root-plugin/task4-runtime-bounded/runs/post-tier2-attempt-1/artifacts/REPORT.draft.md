# sc:sc-reflect — UC-2 post-execution deviation audit (DRAFT, pre-evidence-validator)

```yaml
contract_version: 1.8.0
status: needs_human_decision          # grounding-gaps.yaml non-empty -> contract status: partial
mode: post
tier_reached: 2
confidence_calibrated: 0.90           # Wave 1D blind calibration of the T1 card; Tier-2 cards calibrated 0.92 / 0.91
citations_total: 18
citations_revalidated: TBD
citations_dropped: TBD
citations_inferred: 3
citation_budget_policy: full_reread
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: no-side-effect-requirements
```

Audit root: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project` (git init only, zero commits, all files untracked). Unless a citation is absolute, its path is relative to this root. Inputs: `--diff changes.patch`, `--spec spec.md`, `--tasklist completed.md`, `--scope src`; linked evidence `tests/test_greeting.py`.

## Verdict

- **No deviation in any of the four classes:** Authorized 0, Necessary 0, Drift 0, Regression 0. The single hunk maps to T-101 and T-102 and contradicts no acceptance criterion. Drift = 0 holds only within the supplied diff (GG-3).
- **R-001 and R-002 are met on a static reading.** R-003 is **open**: the tests exist on disk but were never run, and their provenance is unproven.
- Status is therefore `partial` with `needs_human_decision: true`. The empty ledger is **not** an acceptance.
- Tier 2 ran: two heterogeneous `sc:reflect-reviewer` agents (sonnet; haiku slot = grok-4.7), merged by a real `sc:sc-adversarial-protocol` Mode A debate. The merge converged at 18/19 (0.947) but its status is **BLOCKED_BY_INVARIANTS**, because HIGH invariant INV-004 was not addressed in any debate round.

## Evidence (citations)

| ID | Citation | Claim |
|----|----------|-------|
| E-01 | spec.md:5-6 | R-001: greet MUST return the exact string Hello, Ada! for Ada. |
| E-02 | spec.md:8-9 | R-002: greet MUST reject an empty name with ValueError. |
| E-03 | spec.md:11-12 | R-003: tests MUST exercise the ordinary greeting and empty-input rejection. |
| E-04 | completed.md:2 | Tasklist frontmatter declares `status: done`. |
| E-05 | completed.md:6-8 | T-101, T-102 and T-103 are all marked `[x]`. |
| E-06 | changes.patch:1-4 | The patch's only file header is for `src/greeting.py` (new file). There is no hunk for `tests/test_greeting.py`. |
| E-07 | changes.patch:5-9 | One hunk: line 5 is the `@@ -0,0 +1,4 @@` header and lines 6-9 are the 4-line body. |
| E-08 | src/greeting.py:2-3 | `if not name: raise ValueError("name required")`, which satisfies R-002 for `""`. |
| E-09 | src/greeting.py:4 | `return f"Hello, {name}!"`, which yields `Hello, Ada!` for `Ada` (R-001). |
| E-10 | tests/test_greeting.py:1 | The test imports with `from src.greeting import greet`. |
| E-11 | tests/test_greeting.py:4-5 | `test_ordinary` asserts `greet("Ada") == "Hello, Ada!"`. |
| E-12 | tests/test_greeting.py:8-13 | `test_empty` uses try/except (passes on any ValueError; no `pytest.raises`, no message check). |
| E-13 | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/provenance-manifest.json:8-13 | Coverage basis: repo has zero commits, all files untracked; enumeration complete; discovery scopes start at line 13 (`src`). |
| E-14 | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/plugin/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:62 | Drift signal: "Diff hunk does NOT map to any tasklist item." |
| E-15 | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/plugin/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:105-113 | Exit-code table: 1 Regression; 2/3 Grounding Gap; 5 Drift/coverage; 124 Grounding Gap; flaky retry; unmapped Grounding Gap. |
| E-16 | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/plugin/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:149-152 | A non-empty grounding-gaps.yaml forces `status: partial` and `needs_human_decision: true`. |
| E-17 | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/artifacts/task-to-diff-map.md:29-33 | Verification triangle not run (`execute_shell_command` not exposed); no task log; Grounding Gap required. |
| E-18 | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/adversarial/adversarial/debate-transcript.md:237 | Adversarial convergence status BLOCKED_BY_INVARIANTS due to HIGH UNADDRESSED INV-004. |

## Coverage map (task → spec → work)

| Task | Spec | Work | Diff-backed | Verdict |
|------|------|------|-------------|---------|
| T-101 (E-05) | R-001 (E-01) | E-09 | yes (E-07) | adherent (static) |
| T-102 (E-05) | R-002 (E-02) | E-08 | yes (E-07) | adherent (static) |
| T-103 (E-05) | R-003 (E-03) | E-11, E-12 present on disk | **no** (E-06) | open — GG-1, GG-2 |

Claimed completion 3/3 (E-04, E-05). Independently grounded presence 3/3. Execution evidence 0. `tasklist_completion_pct` is therefore 2/3 verified (0.67).

## Deviation register

No deviations: `deviation-ledger.yaml` has zero rows. H1 (E-07) maps to T-101 and T-102, so the Drift signal (E-14) does not match. It contradicts neither R-001 nor R-002, so the Regression signal does not match. Verification did not run (E-17), so no exit code can mint a Regression (E-15). T-103 is a task with no hunk, which is missing provenance rather than an unmapped hunk, so it is not Drift.

## Grounding Gaps

### Gap G-1 — T-103 provenance
- **Hunk ref:** completed.md:8
- **Evidence missing:** no diff hunk for `tests/test_greeting.py` (E-06). Zero commits and an explicitly supplied diff (E-13). No task log.
- **Why not classifiable:** a claim with no hunk is neither Drift (E-14) nor a contradiction.
- **Next evidence needed:** a user attestation or task-log entry saying whether the test file belongs to the audited change. A regenerated or widened diff is **not** acceptable provenance (INV-004).

### Gap G-2 — R-003 execution
- **Hunk ref:** tests/test_greeting.py:1-13
- **Evidence missing:** no pytest exit code or baseline (E-17).
- **Why not classifiable:** presence (E-11, E-12) is not execution (E-03).
- **Next evidence needed:** both invocations' exit codes and per-test outcomes, classified per E-15 (see R-001 below).

### Gap G-3 — scope boundary
- **Hunk ref:** changes.patch:1-9
- **Evidence missing:** only `--scope src` was enumerated (E-13). Root-level and `tests/` files are unknown.
- **Why not classifiable:** an out-of-scope unmapped hunk could neither be cited nor excluded.
- **Next evidence needed:** a user attestation or task log listing every file the work changed.

Non-empty gaps force `partial` + `needs_human_decision` (E-16).

## Risk register

- Grounded: the tests were never executed (E-17). Regression is neither confirmed nor excluded. `regression_present: false` means not observed.
- [INFERRED] Plain `pytest` may fail collection on `from src.greeting import greet` (E-10) when no path config is present. Adding `tests/__init__.py` should fix this under pytest's default prepend import mode, unless there is a root `__init__.py`, a shadowing regular `src` package, or `--import-mode=importlib` (INV-010). Grounded: `src/` contains only `greeting.py` (E-13).
- Grounded: `if not name` (E-08) also rejects `None` and `0` and accepts whitespace-only names. R-002 says only "empty" (E-02), so this is not a contradiction.
- Grounded: `test_empty` (E-12) is a weaker oracle that does not check the error message.
- [INFERRED] A future pytest exit 1 has no previously-passing baseline. Attribute the failure to `src/greeting.py` versus the test file before calling it a Regression (INV-008).

## Per-Task Verdicts

### Task T-101
- **Status:** success
- **Deviation class:** none
- **Citations dropped:** TBD
- **Per-task validation strength:** 0.80 (static only)
- **Evidence anchor:** src/greeting.py:4

### Task T-102
- **Status:** success
- **Deviation class:** none
- **Citations dropped:** TBD
- **Per-task validation strength:** 0.80 (static only)
- **Evidence anchor:** src/greeting.py:2-3

### Task T-103
- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** TBD
- **Per-task validation strength:** 0.30 (presence only; no provenance or execution)
- **Evidence anchor:** tests/test_greeting.py:4-13

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred fraction: 3 / 18 = 0.17

## Recommendations

### Recommendation R-001: Run the tests and classify each invocation
- **File:** n/a (verifier run from the audit root)
- **Change:** run `python -m pytest tests/test_greeting.py -rA` and `pytest tests/test_greeting.py -rA`. Keep the exit codes and per-test outcomes.
- **Verifier:** classify each invocation with E-15:
  - **Exit 1:** retry once first. Count it as a Regression only if the failure is attributed to `src/greeting.py`.
  - **R-003 closes** only on exit 0 with `test_ordinary` and `test_empty` passed and 0 skipped/xfailed/deselected, for both invocations.
- **Linked deviation(s):** none (closes G-2)
- **Priority:** P0

### Recommendation R-002: Supply provenance by attestation, not by a regenerated diff
- **File:** task log or a written user attestation
- **Change:** state whether `tests/test_greeting.py` and any file outside `src/` were produced by the audited work.
- **Verifier:** re-run `/sc:sc-reflect` with `--task-log <path>`, and check that G-1 and G-3 close on the cited entry. Do not regenerate `changes.patch` from the untracked tree.
- **Linked deviation(s):** none (closes G-1, G-3)
- **Priority:** P0

### Recommendation R-003: Fix collection only if plain pytest exits 2
- **File:** tests/__init__.py (or a root pytest config with `pythonpath = .`, which needs pytest ≥ 7)
- **Change:** add the package marker or the path config. Record it as new work.
- **Verifier:** plain `pytest` collects 2 tests. Then re-run R-001.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-004: Clarify "empty" in R-002
- **File:** spec.md (R-002, lines 8-9)
- **Change:** say whether whitespace-only and non-string names count as empty.
- **Verifier:** spec review. If yes, add matching tests and re-run R-001.
- **Linked deviation(s):** none
- **Priority:** P2
