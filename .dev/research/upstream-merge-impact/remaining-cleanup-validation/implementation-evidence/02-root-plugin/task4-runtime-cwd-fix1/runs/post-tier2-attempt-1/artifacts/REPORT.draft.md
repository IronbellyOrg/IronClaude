# /sc:sc-reflect — UC-2 post-execution audit (DRAFT, pre-evidence-gate)

```yaml
contract_version: 1.8.0
status: needs_human_decision        # contract status: partial (grounding gaps non-empty; adversarial convergence blocked)
mode: post
tier_reached: 2
confidence_calibrated: 0.92         # blind-calibrated C of the adversarially selected base card (reviewer-2); reviewer-1 0.90; T1 0.93
citations_total: 18
citations_revalidated: PENDING
citations_dropped: PENDING
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

Citation base: bare paths are relative to `audit_repo_root=/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/fixtures/project`. `<OUT>` = `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts`. `<TAX>` = `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/plugin/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`. Reviewer citations into the frozen snapshot were translated back to these original locations through `<OUT>/reviewer-snapshot/provenance-manifest.json` (byte-identical, verified pre-dispatch, post-review and at Wave 5).

## Verdict summary

The supplied diff (one new file) satisfies T-101/R-001 and T-102/R-002 by static reading. T-103/R-003 (tests) is not evidenced by the supplied diff. No deviation falls into any of the four taxonomy classes (Authorized 0, Necessary 0, Drift 0, Regression 0). Three Grounding Gaps remain, so the run is `partial` with `needs_human_decision: true`. The tasklist frontmatter `status: done` is not supported (diff-backed completion 2/3 = 0.667; executed coverage 0/3). Nothing was executed: the verification triangle was unavailable.

## Task/spec-to-work map

| Task | Spec | Evidence | Verdict |
|---|---|---|---|
| T-101 | R-001 [C4] | [C1] single hunk; [C3] `return f"Hello, {name}!"` | satisfied (static) |
| T-102 | R-002 [C5] | [C2] `if not name: raise ValueError("name required")` | satisfied for `""` (static) |
| T-103 [C8] | R-003 [C6] | no hunk: [C14] `mapped_hunks: []`; file on disk [C10]; self-report [C11]; no run [C12] | not evidenced by diff (G1, G2) |

Frontmatter claim: [C7] `status: done` — not supported.

## Deviation register

None. [C14] records `unmapped_hunks: []` for the only hunk [C1], and no spec criterion is contradicted ([C2]–[C6]); Drift and Regression signals are absent, and there is no divergence to authorize or excuse. Ledger: `<OUT>/deviation-ledger.yaml`.

## Grounding Gaps

Per [C15], a non-empty gap set forces `status: partial` and `needs_human_decision: true`.

### Gap G1
- **Hunk ref:** completed.md:8 / tests/test_greeting.py:1-13 (no changes.patch hunk)
- **Evidence missing:** the diff [C1] contains only src/greeting.py; the test file [C10] has no hunk; [C11] is a self-report and [C12] disclaims execution. Untracked status is not distinctive: [C13] shows every file is untracked and there is no HEAD.
- **Why not classifiable:** no contradiction and no unmapped hunk; the gap is explained by the `--scope src` audit boundary, so it is an evidence-supply gap, not proof of non-delivery.
- **Next evidence needed:** a regenerated diff with scope beyond src/ containing the test hunk, or explicit user confirmation.

### Gap G2
- **Hunk ref:** tests/test_greeting.py:1 [C9] / src/greeting.py:1-4
- **Evidence missing:** no test run [C12]; no package marker or pytest config in the audit root [C13].
- **Why not classifiable:** [INFERRED] `from src.greeting import greet` resolves under `python -m pytest` from the root but may fail collection under plain pytest; a collection error is a Grounding Gap, not a Regression [C16]. Not observed.
- **Next evidence needed:** outputs of both pytest invocations from the audit root.

### Gap G3
- **Hunk ref:** src/greeting.py:2-3 [C2] (R-002 [C5])
- **Evidence missing:** the spec does not define "empty" for None, 0, whitespace-only or non-str input.
- **Why not classifiable:** nothing is contradicted and the line maps to T-102; behavior on other falsy or whitespace input is unspecified. Reviewer-1 argued for the advisory correctness-gaps channel; the merged verdict kept it here.
- **Next evidence needed:** a spec clarification of R-002.

## Tier-2 ensemble and adversarial merge

- Reviewers (fixed `sc:reflect-reviewer`, read-only, frozen native snapshot): reviewer-1 analyzer / sonnet slot, blind-calibrated C=0.90; reviewer-2 qa / haiku slot (env `grok-4.7[1m]`), C=0.92. Calibrator: `sc:confidence-calibrator` on the opus slot (outside reviewer classes → `calibrator_diversity: full`). Both reviewers independently reached 0 deviations, 3 gaps, completion 0.667, `regression_present: false`.
- `Skill sc:sc-adversarial-protocol` Mode A (`merge_method: adversarial`): attempt 1 was interrupted after Round 1 (evidence preserved); attempt 2 completed Round 2, the Round 2.5 invariant probe, scoring, refactor plan and the `sc:merge-executor` merge. Producer status is **partial**: diff-point agreement 17/17 = 1.0, but convergence is **BLOCKED_BY_INVARIANTS** by HIGH invariant INV-006 [C17][C18]. Base: reviewer-2 (combined 0.944 vs 0.819).
- INV-006: a bare "pytest exit 1 = Regression" rule would let a tool/environment failure falsely set `regression_present`; the taxonomy maps exits individually and requires a flaky retry [C16]. The merged recommendation R-002 below carries the full mapping, but the debate itself never ruled on it, so it stays unaddressed.

## Degradation and coverage notes

- MCP: Serena and Auggie not exposed → native Read/Grep/Glob grounding; reuse search degraded (`neighbour-search:auggie_unavailable`, no prior art found); reviewer snapshot MCP-unindexed.
- Verification triangle did not run (`verification_skip_reason: tool-unavailable`); Regression detection degraded to the task log, which claims no execution [C12].
- Runtime-surface sweep not applicable (plain function); contracted-sink reachability skipped (`no-side-effect-requirements`).
- Executor model class unresolved → anti-self-confirmation guarantee weakened.
- `proposed.md` (unsupplied, untracked [C13]) was not in the reviewer snapshot; reviewers noted it restates T-101..T-103 only.
- Producer-reported deviation: the merge-executor validated YAML via `uv run --no-project --with pyyaml` (temporary environment from the local uv cache), in tension with the no-installs boundary.

## Inferred-claim audit

- `citations_inferred: 2` (G2 import-resolution behavior; the reviewer-2 static pass prediction carried in the merged card)
- Inferred-fraction: 2 / 18 = 0.11

## Recommendations

### Recommendation R-001: Regenerate the audited diff with the test file in scope
- **File:** changes.patch (audit root)
- **Change:** produce one patch covering src/greeting.py and tests/test_greeting.py with scope widened beyond `src/`; with no HEAD [C13], a tests-only intent-to-add would drop the existing hunk.
- **Verifier:** a rebuilt Wave 1B map keeps H1 → T-101/T-102 and maps a new hunk matching tests/test_greeting.py:1-13 to T-103 (no longer `mapped_hunks: []` [C14]); then G1 can close.
- **Linked deviation(s):** none (G1)
- **Priority:** P0

### Recommendation R-002: Run both pytest invocations and classify per the full exit-code table
- **File:** tests/test_greeting.py
- **Change:** the user runs `python -m pytest tests -q` and plain `pytest tests -q` from the audit root and records both outputs; prefer fixing an import failure by invocation over adding unmapped files.
- **Verifier:** classify per [C16]: exit 0 (2 passed) clears G2; exit 1 is a Regression only if tests were collected and an assertion failed (retry once first); 2/3, 124 and unmapped → Grounding Gap; 5 → Drift/coverage. Disagreeing invocations keep G2 open.
- **Linked deviation(s):** none (G2; INV-006)
- **Priority:** P0

### Recommendation R-003: Stop the tasklist claiming T-103 done until evidence exists
- **File:** completed.md
- **Change:** set frontmatter `status` [C7] to partial and uncheck T-103 [C8] until R-001 and R-002 are satisfied; take a fresh snapshot before re-audit.
- **Verifier:** completed.md:2 reads `done` only after the test hunk is in the diff and a run is recorded.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-004: Clarify R-002 semantics before changing code
- **File:** spec.md
- **Change:** state behavior for None, non-str and whitespace-only names at spec.md:9 [C5]; only then adjust src/greeting.py:2 [C2] and add assertions.
- **Verifier:** spec.md:9 amended and each stated case has a passing assertion; G3 closes.
- **Linked deviation(s):** none (G3)
- **Priority:** P2

## Citation index (for the evidence gate)

| ID | Citation | Claim |
|---|---|---|
| C1 | changes.patch:5-9 | the only hunk: new file src/greeting.py, 4 added lines |
| C2 | src/greeting.py:2-3 | `if not name:` / `raise ValueError("name required")` |
| C3 | src/greeting.py:4 | `return f"Hello, {name}!"` |
| C4 | spec.md:6 | R-001: greet MUST return exactly "Hello, Ada!" for Ada |
| C5 | spec.md:9 | R-002: MUST reject an empty name with ValueError |
| C6 | spec.md:12 | R-003: tests MUST exercise ordinary greeting and empty-input rejection |
| C7 | completed.md:2 | frontmatter `status: done` |
| C8 | completed.md:8 | `[x] T-103 implements R-003 both ordinary and empty-input tests` |
| C9 | tests/test_greeting.py:1 | `from src.greeting import greet` |
| C10 | tests/test_greeting.py:4-13 | test_ordinary and test_empty |
| C11 | execution.log:4 | log claims T-103 created tests/test_greeting.py |
| C12 | execution.log:5 | "No test execution is claimed" |
| C13 | `<OUT>/artifacts/git-inventory.txt:2-9` | all files untracked incl. src/greeting.py and proposed.md; no HEAD revision; no package marker/pytest config listed |
| C14 | `<OUT>/artifacts/task-diff-map.yaml:23-29` | T-103 `mapped_hunks: []`; `unmapped_hunks: []` |
| C15 | `<TAX>:149-153` | non-empty grounding-gaps forces partial + needs_human_decision |
| C16 | `<TAX>:105-113` | per-tool exit-code → class table (exit 1 Regression; 2/3, 124, flaky, unmapped → Grounding Gap; 5 → Drift/coverage) |
| C17 | `<OUT>/adversarial/adversarial/invariant-probe.md:17` | INV-006 guard_conditions, UNADDRESSED, HIGH |
| C18 | `<OUT>/adversarial/adversarial/return-contract.yaml:4-10` | BLOCKED_BY_INVARIANTS; convergence_score 1.0 (agreement only); status partial |
