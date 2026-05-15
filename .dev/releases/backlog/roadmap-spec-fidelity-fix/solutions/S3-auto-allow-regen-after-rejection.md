# Solution S3 (refactored) — Tiered Diff-Size Relaxation Across Convergence Runs

> **Refactored 2026-05-15 after adversarial review.** Original draft is
> preserved at the bottom of this file for traceability. The original
> proposal misdiagnosed the documented failure (the 10 surviving HIGHs
> were structural false positives, not diff-size rejections — see
> `agent-reports/S3-debate.md` §1–2 for evidence). This refactor:
> (a) reframes S3 as a *defensive convergence-tier feature* for the
> >30%-rejection failure shape that the loop *will* hit on future
> runs, not the current run; (b) adds policy nuance (tiered, gated,
> reversible); (c) defends against deletion attacks the original
> ignored; (d) keeps FR-9 invariants intact via opt-in flags.

## Failure shape this solution actually addresses

A future run where Run 1's remediation agent proposes a structurally
correct patch that exceeds the 30% threshold for one or more files,
gets rejected, and Run 2 / Run 3 then repeat the rejection because
`config.allow_regeneration` is set once at CLI parse time. This is the
*"71.3% → 38.1% rejection"* pattern in the failure summary but **not**
the *"15 → 15 → 10"* pattern in the current registry.

Solutions for the actual current failure (greedy spec parser emitting
findings against non-paths and unaddressable NFR primitives) live in
S1/S2/S4. S3 is complementary, not a substitute.

## Target root cause (revised)

`convergence.execute_fidelity_with_convergence` (`convergence.py:386`)
invokes a `run_remediation(registry)` callable that closes over
`PipelineConfig.allow_regeneration` at construction time
(`executor.py:1395-1446`). The convergence loop has run-index awareness
(`run_idx`, `run_label`) but cannot vary the diff-size policy per run.
That is a real plumbing gap, regardless of whether the current failure
exercises it.

## Proposal — tiered, gated, reversible

### A. Plumbing change (signature)

Extend the convergence protocol so `run_remediation` receives the run
index and a derived `RegenerationPolicy`. The convergence loop
constructs the policy from config + prior-run telemetry, never from
arbitrary heuristics.

```python
# convergence.py — inside execute_fidelity_with_convergence
policy = _resolve_regen_policy(
    run_idx=run_idx,
    config=config,
    prior_run_summary=structural_progress[-1] if structural_progress else None,
    active_high_count=active_highs,
)
ledger.debit(REMEDIATION_COST)
run_remediation(registry, regen_policy=policy)
```

```python
# new dataclass in models.py
@dataclass(frozen=True)
class RegenerationPolicy:
    threshold_pct: int           # 30, 60, or 100
    allow_regeneration: bool     # True only when threshold_pct == 100
    reason: str                  # for logging — required, non-empty
    arming_run_idx: int          # which prior run armed this relaxation
```

`executor.py:1395` (`_run_remediation` closure) updates its signature
to `(reg, *, regen_policy)` and forwards both fields into
`execute_remediation(..., diff_threshold_pct=policy.threshold_pct,
allow_regeneration=policy.allow_regeneration)`. The threshold becomes a
parameter rather than a module constant.

### B. Tier policy (the actual relaxation curve)

| Run | Threshold | `allow_regeneration` | Arming condition |
|-----|-----------|----------------------|------------------|
| 1 (catch) | 30% (FR-9) | False | Always |
| 2 (verify) | 60% | False | Run 1 rejected ≥1 patch by diff-size guard AND active_high_count ≥ 3 |
| 3 (backup) | 100% (off) | True | Run 2 also failed to reduce structural HIGH count AND active_high_count ≥ 3 |

Run 1 stays strict, full stop. Run 2 raises the cap to 60% only when
the rejection telemetry from Run 1 shows the cap was actually hit;
otherwise stay at 30%. Run 3 only opens the gate fully when Run 2 made
no progress — exactly mirroring the convergence loop's existing
structural-progress invariant.

### C. Finding-set-size heuristic

If `active_high_count < 3` at the start of Run 2 or Run 3, the policy
**stays at 30%** regardless of rejection telemetry. Rationale: a
1-or-2-finding case never justifies a section rewrite; the LLM is
strictly more likely to introduce regressions than to fix the case.
This also blocks a class of pathological "single typo → full rewrite"
spirals.

### D. Deletion-attack defence

Before accepting any patch under a relaxed policy (`threshold_pct >
30`), run a structural pre/post diff on the target file:

```python
def is_likely_deletion_fix(pre: str, post: str) -> bool:
    pre_headings = _count_markdown_headings(pre)
    post_headings = _count_markdown_headings(post)
    pre_id_anchors = _count_id_anchors(pre)   # [A-Z]+-\d+ patterns
    post_id_anchors = _count_id_anchors(post)
    return (post_headings < pre_headings * 0.90) or \
           (post_id_anchors < pre_id_anchors * 0.90)
```

If `is_likely_deletion_fix` returns True, force-rollback regardless of
diff-size pass. This closes the attack where the agent satisfies a
"finding X is not in roadmap" by deleting the conflicting section
rather than adding X. The threshold (90%) is conservative; tune via
config if false-positive rate becomes an issue.

### E. CLI surface (FR-9 invariant preserved)

```
--allow-regeneration              # existing — Run 1+ all relaxed (caution)
--convergence-tier-relax          # new — opts into tiered policy (B+C+D)
--convergence-deletion-guard      # new — independent toggle for (D), default ON
```

Default remains: Run 1, Run 2, Run 3 all at 30%, `allow_regeneration=False`.
The tiered behaviour is opt-in. This satisfies the FR-9 contract that
the strict 30% guard is the documented default and any relaxation is
explicit at the CLI.

### F. Telemetry — required

Each run's `runs[]` entry in `deviation-registry.json` gains:
```json
{
  "regen_policy": {
    "threshold_pct": 60,
    "allow_regeneration": false,
    "reason": "Run 1 rejected 2 patches by diff-size; active_highs=12 ≥ 3",
    "arming_run_idx": 1
  },
  "patches_rejected_by_threshold": 2,
  "deletion_guard_triggered": false
}
```

This lets reviewers and downstream gates (anti-instinct,
wiring-verification) tell whether a relaxed run produced the artifact
they're auditing.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Anti-instinct gate sees over-confident prose from regen | Default-on deletion guard; tier opt-in; telemetry surfaces relaxation in audit reports |
| Wiring-verification breaks due to ID renames under regen | Heading/ID anchor count check in (D) catches >10% drop |
| FR-9 silently weakened | Opt-in flag, default unchanged, doc update mandatory in same PR |
| Mis-armed Run 2 (no Run 1 rejection but relaxes anyway) | Arming condition checks rejection telemetry, not just run index |
| Single-finding pathology | Finding-set-size floor of 3 |
| False positive in deletion guard | Configurable threshold; logged not silent; user can disable per-run |

## What this does NOT fix

- The greedy `parse_document(...).file_paths` parser emitting structural
  findings against `'src/x.py:88\`'`, `'docs/error-grouping-best-practices'`,
  brace expansions, etc. **This is the actual cause of the documented
  3-run failure.** Address via S1/S2/S4 (parser tightening or
  ignore-list).
- Unaddressable NFR primitives (`encryption`, `hash`, `<1%`) being
  reported as missing when the spec uses them as cross-cutting concerns
  rather than first-class NFRs. Same parser-side fix needed.

## Expected impact

- On the *current* 15→15→10 failure: **none.** S3 alone leaves Run 1, 2,
  3 all at threshold 30% because the arming condition (Run 1 rejection)
  never fires. Combined effect = no regression, no gain.
- On a *future* 71%-rejection-style failure: Run 2 relaxes to 60% if
  warranted, Run 3 to 100% if Run 2 stalled, with deletion-attack
  defence active. Convergence rate on that failure class should
  meaningfully improve (rough estimate: rejection-driven failures drop
  to ≤1 in the convergence loop).

## Estimated effort

- `models.py`: +1 dataclass, +1 field on `PipelineConfig` (~20 LOC)
- `convergence.py`: signature update, `_resolve_regen_policy` helper (~40 LOC)
- `executor.py`: `_run_remediation` closure update (~10 LOC)
- `remediate_executor.py`: thread `diff_threshold_pct` through
  `execute_remediation`, `check_patch_diff_size`, `_check_diff_size`
  (~20 LOC); add `is_likely_deletion_fix` + pre/post comparison (~40 LOC)
- `commands.py`: 2 new flags (~10 LOC)
- Tests: 6 new tests (tier policy matrix, deletion guard, opt-in
  default, single-finding floor, telemetry, FR-9 default unchanged)
- Time: ~2 hours including tests.

## Files touched

- `src/superclaude/cli/roadmap/convergence.py`
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/remediate_executor.py`
- `src/superclaude/cli/roadmap/commands.py`
- `src/superclaude/cli/roadmap/models.py`
- `tests/cli/roadmap/test_convergence.py`
- `tests/cli/roadmap/test_remediate_executor.py`

## Confidence

- Standalone (for the future >30%-rejection failure shape): **72%**
- Combined with S1/S2/S4 (parser tightening) for the documented current
  failure: **78%**

---

## Original draft (preserved for traceability)

```
# Solution S3 — Auto-Enable allow-regeneration After First Rejection

## Target root cause
Run 1 of convergence is supposed to be conservative; Runs 2–3 are
"verify" and "backup". Today, all three runs use the same 30%
threshold, so once a patch is rejected at Run 1 the rejection
recurs at Run 2 and Run 3 with zero progress.

## Proposal
In `convergence.execute_fidelity_with_convergence`, pass a
`run_idx`-aware `allow_regeneration` flag into the remediation
function:

    effective_allow_regen = config.allow_regeneration or (run_idx >= 1)
    run_remediation(registry, allow_regeneration=effective_allow_regen)

Rationale:
- Run 1 (catch): strict 30% guard — favours minimal patches.
- Run 2 (verify): if patches were rejected at Run 1, allow regeneration
  so the agent can rewrite the affected section wholesale.
- Run 3 (backup): always allow regeneration as the last shot.

Additionally, expose this as a CLI flag pair:
    --strict-convergence          # disable the auto-relax (current behavior)
    --convergence-relax-after N   # default 1

## Risks / downsides
- Allowing regeneration removes the safety net that prevents the agent
  from nuking the file. Mitigation: the per-file rollback still
  applies if the agent produces an invalid document.
- May mask genuine bugs in patch generation (agent producing huge
  unrelated diffs).
- Backward compatibility: existing CI may rely on strict 30% — gate
  behind a config flag with a deprecation cycle.

## Expected impact on the failing case
- Run 1: 15 HIGHs, rejected patches → 15 HIGHs unchanged.
- Run 2 (with auto-relax): wholesale rewrite of TDD/roadmap section
  permitted, structural HIGHs drop sharply.
- Run 3: cleanup.

Alone, S3 still wastes Run 1, but combined with S1+S2 it converges in 2 runs.

## Estimated effort
- Code: ~15 LOC in convergence.py + signature change
- Tests: 2 new convergence tests
- Time: 25 min

## Files touched
- src/superclaude/cli/roadmap/convergence.py
- src/superclaude/cli/roadmap/remediate_executor.py (parameter plumbing)
- src/superclaude/cli/roadmap/commands.py (new flag)
- tests/cli/roadmap/test_convergence.py
```
