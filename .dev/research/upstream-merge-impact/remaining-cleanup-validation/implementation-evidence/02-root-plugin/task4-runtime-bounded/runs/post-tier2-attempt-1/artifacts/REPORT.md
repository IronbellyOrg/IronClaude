# sc:sc-reflect — UC-2 post-execution deviation audit

```yaml
contract_version: 1.8.0
status: needs_human_decision          # grounding-gaps non-empty; return-contract status: partial
mode: post
tier_reached: 2
confidence_calibrated: 0.90           # Wave 1D independent blind calibration (opus) of the Tier-1 card; Tier-2 cards 0.92 / 0.91
citations_total: 25
citations_revalidated: 25
citations_dropped: 1                  # E-13 (range off-by-one) — dropped by sc:evidence-validator
citations_inferred: 2
citation_budget_policy: full_reread
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: no-side-effect-requirements
```

**Audit root:** `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project`. The repo has had `git init` only: zero commits, all files untracked. Citation paths are relative to this root unless shown as absolute. `OUT` means `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts`, and `PLUGIN` means `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/plugin`.

**Inputs:**
- `--diff changes.patch`, `--spec spec.md`, `--tasklist completed.md`, `--scope src`.
- Linked evidence: `tests/test_greeting.py`.
- Not supplied, and not used as evidence: `execution.log`, `proposed.md`.

## Verdict

- **No deviation in any of the four classes:** Authorized 0, Necessary 0, Drift 0, Regression 0.
  - The single hunk maps to T-101 and T-102 and contradicts no acceptance criterion.
  - Drift = 0 holds only within the supplied diff (GG-3).
- **R-001 and R-002 are met on a static reading.** R-003 is **open**: the tests exist on disk, but they were never run and their provenance is unproven.
- **Status:** `partial`, with `needs_human_decision: true`. The empty ledger is **not** an acceptance.
- **Tier 2 merge:**
  - Ran with two `sc:reflect-reviewer` agents on different model classes: analyzer on sonnet (`claude-sonnet-5-5[1m]`) and qa on the haiku slot, which resolves to `grok-4.7[1m]`.
  - The cards were merged by a real `sc:sc-adversarial-protocol` Mode A debate.
  - Convergence was 18/19 (0.947), but the status is **BLOCKED_BY_INVARIANTS**. The HIGH invariant INV-004 was raised by the fault-finder and not addressed in any debate round (E-18).

## Evidence (citations)

| ID | Citation | Claim |
|----|----------|-------|
| E-01 | spec.md:5-6 | R-001: greet MUST return the exact string Hello, Ada! for Ada. |
| E-02 | spec.md:8-9 | R-002: greet MUST reject an empty name with ValueError. |
| E-03 | spec.md:11-12 | R-003: Tests MUST exercise the ordinary greeting and empty-input rejection. |
| E-04 | completed.md:2 | Tasklist frontmatter declares `status: done`. |
| E-05 | completed.md:6-8 | T-101, T-102 and T-103 are all marked `[x]`. |
| E-06 | changes.patch:1-4 | The patch's only file header is for `src/greeting.py` (new file). There is no hunk for `tests/test_greeting.py`. |
| E-07 | changes.patch:5-9 | One hunk: line 5 is the `@@ -0,0 +1,4 @@` header, and lines 6-9 are the 4-line body. |
| E-08 | src/greeting.py:2-3 | `if not name: raise ValueError("name required")`. This satisfies R-002 for `""`. |
| E-09 | src/greeting.py:4 | `return f"Hello, {name}!"` yields `Hello, Ada!` for `Ada` (R-001). |
| E-10 | tests/test_greeting.py:1 | The test imports with `from src.greeting import greet`. |
| E-11 | tests/test_greeting.py:4-5 | `test_ordinary` asserts `greet("Ada") == "Hello, Ada!"`. |
| E-12 | tests/test_greeting.py:8-13 | `test_empty` uses try/except. It passes on any ValueError; there is no `pytest.raises` and no message check. |
| ~~E-13~~ | ~~OUT/reviewer-snapshot/provenance-manifest.json:8-13~~ | **DROPPED by sc:evidence-validator**: off-by-one range. Replaced by E-13a. |
| E-13a | OUT/reviewer-snapshot/provenance-manifest.json:8-9, 13-14, 45-50 | Line 8: zero commits, all files untracked, explicit `--diff`, and execution.log/proposed.md not supplied. Line 9: enumeration complete. Lines 13-14: discovery scopes `["src"]`. Lines 45-50: the scoped inventory contains only `src/greeting.py`. These are the line locations the validator gave; the orchestrator re-Read them before finalizing. |
| E-14 | PLUGIN/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:62 | Drift signal: "Diff hunk does NOT map to any tasklist item." |
| E-15 | PLUGIN/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:105-113 | Exit-code table: 1 = Regression; 2/3 = Grounding Gap; 5 = Drift/coverage; 124 = Grounding Gap; flaky means retry once; any unmapped code = Grounding Gap. |
| E-16 | PLUGIN/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:149-152 | A non-empty grounding-gaps file forces `status: partial` and `needs_human_decision: true`. |
| E-17 | OUT/artifacts/task-to-diff-map.md:29-33 | The verification triangle was not run (`execute_shell_command` not exposed) and no `--task-log` was supplied, so a Grounding Gap is required. |
| E-18 | OUT/adversarial/adversarial/debate-transcript.md:237 | Adversarial convergence status is BLOCKED_BY_INVARIANTS because of the HIGH UNADDRESSED INV-004. |

## Coverage map (task → spec → work)

| Task | Spec | Work | Diff-backed | Verdict |
|------|------|------|-------------|---------|
| T-101 (E-05) | R-001 (E-01) | E-09 | yes (E-07) | adherent (static) |
| T-102 (E-05) | R-002 (E-02) | E-08 | yes (E-07) | adherent (static) |
| T-103 (E-05) | R-003 (E-03) | E-11, E-12 present on disk | **no** (E-06) | open (GG-1, GG-2) |

- **Claimed completion:** 3/3 (E-04, E-05).
- **Presence grounded independently:** 3/3.
- **Execution evidence:** 0.
- **`tasklist_completion_pct`:** 0.67 (2/3 independently verified). The orchestrator derived this figure; it was not calibrated.

## Deviation register

`deviation-ledger.yaml` has zero rows.
- **Not Drift:** H1 (E-07) maps to T-101 and T-102, so the Drift signal (E-14) does not match.
- **Not Regression:** H1 contradicts neither R-001 nor R-002. Verification did not run (E-17), so no exit code can mint a Regression (E-15).
- **T-103:** this is a task with no hunk, which is missing provenance rather than an unmapped hunk. It is not Drift.

## Grounding Gaps

### Gap GG-1: T-103 provenance
- **Hunk ref:** completed.md:8
- **Evidence missing:**
  - No diff hunk for `tests/test_greeting.py` (E-06).
  - Zero commits, and the diff was supplied explicitly (E-13a).
  - No `--task-log` was supplied. `execution.log` exists in the audit root but was not an input.
- **Why not classifiable:** a completion claim with no hunk is neither Drift (E-14) nor a contradiction.
- **Next evidence needed:** a user attestation or a task-log entry saying whether the test file belongs to the audited change. A regenerated or widened diff is **not** acceptable provenance (INV-004).

### Gap GG-2: R-003 execution
- **Hunk ref:** tests/test_greeting.py:1-13
- **Evidence missing:** no pytest exit code and no baseline (E-17).
- **Why not classifiable:** presence (E-11, E-12) is not execution (E-03).
- **Next evidence needed:** exit codes and per-test outcomes from both invocations, classified per E-15 (Rec-1).

### Gap GG-3: scope boundary
- **Hunk ref:** changes.patch:1-9
- **Evidence missing:** only `--scope src` was enumerated (E-13a). Root-level and `tests/` files are unknown.
- **Why not classifiable:** an out-of-scope unmapped hunk can be neither cited nor excluded.
- **Next evidence needed:** a user attestation or task log listing every file the work changed.

The non-empty gaps force `partial` and `needs_human_decision` (E-16).

## Risk register

- **Grounded:** the tests were never executed (E-17). A Regression is neither confirmed nor excluded. `regression_present: false` means "not observed", not "absent".
- [INFERRED] **Collection failure:** plain `pytest` may fail to collect `from src.greeting import greet` (E-10) when no path config exists.
  - Adding `tests/__init__.py` should fix it under pytest's default prepend import mode.
  - It would not fix it if there is a root `__init__.py`, a shadowing regular `src` package, or `--import-mode=importlib` (INV-010).
  - **Grounded:** `src/` contains only `greeting.py` (E-13a).
- **Grounded:** `if not name` (E-08) also rejects `None` and `0`, and it accepts whitespace-only names. R-002 says only "empty" (E-02), so this is not a contradiction.
- **Grounded:** `test_empty` (E-12) is a weaker oracle, with no message check.
- [INFERRED] **Exit 1 without a baseline:** a future pytest exit 1 has no previously-passing baseline. Before calling it a Regression, attribute the failure to `src/greeting.py` or to the test file (INV-008).

## Per-Task Verdicts

Validation strengths are orchestrator-derived from the calibrated card scores and the evidence grade. They are not independently calibrated.

### Task T-101
- **Status:** success
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.80 (static only)
- **Evidence anchor:** src/greeting.py:4

### Task T-102
- **Status:** success
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.80 (static only)
- **Evidence anchor:** src/greeting.py:2-3

### Task T-103
- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** 1 (E-13 supported GG-1; re-cited as E-13a)
- **Per-task validation strength:** 0.30 (presence only; no provenance and no execution)
- **Evidence anchor:** tests/test_greeting.py:4-13

## Degradation and process disclosures

- **MCP and tools:**
  - Serena, Auggie, Context7 and Tavily were not exposed. Grounding used native Read/Grep/Glob.
  - The verification triangle was skipped (`tool-unavailable`).
  - No memory was hydrated or persisted.
  - `think_about_*` checkpoints were skipped.
- **Executor class:** not resolved, so the anti-self-confirmation guarantee is weakened. Pass `--executor-model` to enforce it.
- **Reviewer snapshot:** native-selected-inputs, MCP-unindexed. It was verified before dispatch, after review and at Wave 5, with no drift. The input tree hash is unchanged (`e7a7e775…c453`).
- **Same-model condition:** the adversarial advocates, scorers, fault-finder and judge all ran on opus, the Mode A default advocate model, so the judge and debaters share a class. The calibrators were also opus, which is disjoint from the reviewer classes.
- **Brief deviations:** two delegated workers made read-only shell reads inside their allowed paths although their briefs said no shell. These were the Round-2 V2 advocate and `sc:merge-executor`. Neither wrote anything outside its allowed files.
- **Not written:** `.dev/reflect/runs.jsonl` was not written, because it is outside the pinned output.

## Inferred-claim audit

- `citations_inferred: 2`
- Inferred fraction: 2 / 25 = 0.08

## Recommendations

> sc:confidence-check scored **0.40**, below 0.70, so `blocked_by_low_confidence: true`. These recommendations are advisory. pytest is not installed here and no docs or search tools were available, so pytest-specific tokens are **[UNVERIFIED]**. Confirm them with `pytest --version` and `pytest --help`.

### Recommendation Rec-1: Run the tests and classify each invocation
- **File:** n/a (a verifier run from the audit root)
- **Change:**
  - Run `python -m pytest tests/test_greeting.py -rA` and `pytest tests/test_greeting.py -rA`. The `-rA` flag is [UNVERIFIED].
  - Keep the exit codes and per-test outcomes.
- **Verifier:**
  - Classify each invocation separately with E-15.
  - On exit 1, retry once. Count it as a Regression only if the failure is attributed to `src/greeting.py`.
  - R-003 closes only if both invocations exit 0 with `test_ordinary` and `test_empty` passed and nothing skipped, xfailed or deselected.
- **Linked:** closes GG-2.
- **Priority:** P0

### Recommendation Rec-2: Supply provenance by attestation or task log, not by a regenerated diff
- **File:** a task log or a written user attestation
- **Change:**
  - State whether `tests/test_greeting.py`, and any file outside `src/`, came from the audited work.
  - `execution.log` (line 4) claims T-103 created the test file. If you confirm it is authoritative, supply it as `--task-log execution.log`. Line 5 claims no test execution, so it would not close GG-2.
- **Verifier:**
  - Re-run `/sc:sc-reflect` with `--task-log`, and confirm GG-1 and GG-3 close on the cited entry.
  - Never regenerate `changes.patch` from the untracked tree.
- **Linked:** closes GG-1 and GG-3.
- **Priority:** P0

### Recommendation Rec-3: Fix collection only if plain pytest exits 2
- **File:** `tests/__init__.py`, or a root pytest config with `pythonpath = .` (pytest 7+ [UNVERIFIED])
- **Change:** add the marker or the config, and record it as new work.
- **Verifier:** plain `pytest` collects 2 tests. Then re-run Rec-1.
- **Linked:** none
- **Priority:** P1

### Recommendation Rec-4: Clarify "empty" in R-002
- **File:** spec.md (lines 8-9)
- **Change:** state whether whitespace-only and non-string names count as empty.
- **Verifier:** spec review. If they do, add matching tests and re-run Rec-1.
- **Linked:** none
- **Priority:** P2

**Remediation/promotion:** `--remediate` was not requested, so there was no Tier 3. `--no-promote` was honored: Wave 7 was suppressed, nothing was moved and no archive was written.
