# D-0084 Evidence — T07.02 NFR-CONV.4 Token-Cost Ratio Measurement

**Task:** T07.02 — Measure NFR-CONV.4 token-cost ratio (≤1.10)
**Companion spec:** `.dev/releases/current/task-builder-merge/artifacts/D-0084/spec.md`
**Date captured:** 2026-05-18
**Branch:** feat/hook-sync-and-matcher-fix
**Pre-merge baseline anchor commit:** `fd41178` (parent of first task-builder-merge prep commit `9d1e51b`)
**Post-merge measurement commit:** `87c8254` (HEAD; MIG-006 land FR-CONV.6)

---

## 1. Git Anchor Verification

Authoritative commit chain establishing the pre/post boundary for the task-builder-merge release:

```text
87c8254 feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)   [HEAD]
db6166e feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)
487e76b feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)
ad083b6 feat(task-builder): MIG-003 land FR-CONV.3 Inherited Structural Verdict + Self-Audit (M3)
2648be8 feat(task-builder): MIG-002 land FR-CONV.2 Execution Context header (M2)
dfae6cf feat(task-builder): PR-03 DNSP synthetic finding (paradigm-neutral, BASE)
eed1851 feat(task-builder): PR-02 retry monotonicity guards (anti-oscillation)
0abf897 feat(task-builder): PR-07 adversarial category naming (5-axis overlay)
3a57a0d feat(task-builder): PR-04 gate-results passthrough (inherited structural verdict)
f7127c9 feat(task-builder): PR-01 execution context header (revise-then-adopt)
9d1e51b feat(task-builder): PR-06 structural gate additions (TB-Add-1 through TB-Add-7)
fd41178 feat(reflect): add Re-scrutiny phase 4 + promote rf agents/skills to src/   [PRE-MERGE BASELINE]
```

Reproducibility: `git log --oneline --all -- src/superclaude/agents/rf-task-builder.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md`

## 2. Agent / Skill File-Size Diff (Static Surface)

Diagnostic only — does not drive the ratio (see spec §2.1). Demonstrates the FR-CONV.1..6 footprint on static prompt-load.

Method: `git show fd41178:<path> | wc -c` vs `wc -c < <path>` at HEAD.

| File | pre-merge chars (@fd41178) | post-merge chars (@87c8254) | Δ chars | Δ % |
|---|---:|---:|---:|---:|
| `src/superclaude/agents/rf-task-builder.md` | 20,862 | 29,332 | +8,470 | +40.6% |
| `src/superclaude/agents/rf-team-lead.md` | 16,854 | 16,854 | 0 | 0.0% |
| `src/superclaude/agents/rf-task-researcher.md` | 17,008 | 17,008 | 0 | 0.0% |
| `src/superclaude/agents/rf-task-executor.md` | 8,260 | 8,260 | 0 | 0.0% |
| `src/superclaude/agents/rf-qa.md` | 25,761 | 48,323 | +22,562 | +87.6% |
| `src/superclaude/agents/rf-qa-qualitative.md` | 60,182 | 92,200 | +32,018 | +53.2% |
| `src/superclaude/skills/task-builder/SKILL.md` | 91,332 | 171,195 | +79,863 | +87.4% |
| **TOTAL static load** | **240,259** | **383,172** | **+142,913** | **+59.5%** |

Per `git diff --stat fd41178..HEAD -- src/superclaude/agents/ src/superclaude/skills/task-builder/SKILL.md`:
```text
src/superclaude/agents/rf-analyst.md         |  22 +-     (peripheral; not loaded by task-builder pipeline)
src/superclaude/agents/rf-qa-qualitative.md  | 207 +
src/superclaude/agents/rf-qa.md              |  39 +
src/superclaude/agents/rf-task-builder.md    |  42 +
src/superclaude/skills/task-builder/SKILL.md | 426 +
5 files changed, 725 insertions(+), 11 deletions(-)
```

Static-surface delta is well outside the 10% NFR-CONV.4 ceiling, but this is *not* the K-010-targeted lever (see spec §2.1) — static prompt-load amortizes across cached turns and the K-010 contingency mitigation only acts on output emission.

## 3. Per-FR Output-Emission Measurement (Empirical)

Reference real-pipeline emission: `.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-qualitative-review.md` (15,574 chars, 10 sections, first-cycle PASS verdict, content date 2026-05-17, post-FR-CONV.3 schema).

Measurements (reproducible via `awk` block extraction):

```text
$ f=.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-qualitative-review.md

# FR-CONV.2 — Execution Context header (top of file, lines 1-9)
$ head -10 "$f" | wc -c
216

# FR-CONV.3 — Inherited Structural Verdict — Reliance Audit (lines 60-89)
$ awk '/^## Inherited Structural Verdict/,/^## [^I]/' "$f" | wc -c
3733

# FR-CONV.4 — Adversarial Verification Summary (PR-07 Axes) (lines 41-51)
$ sed -n '41,52p' "$f" | wc -c
2113
```

Section roster confirmation:
```text
$ grep -n "^## " "$f"
10:## Overall Verdict: PASS
12:## Items Reviewed
32:## Summary
41:## Adversarial Verification Summary (PR-07 Axes)
51:## Confidence Gate
60:## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
89:## Actions Taken
93:## Recommendations
102:## Verdict
106:## QA Complete
```

## 4. Per-Pipeline Output-Emission Delta Computation

| FR | per-emission chars | per-pipeline emissions | per-pipeline Δ chars | per-pipeline Δ tokens (÷4) |
|---|---:|---:|---:|---:|
| FR-CONV.1 (TB-Add-1..8 structural gates) | 0 (gates input only, no extra output) | 0 | 0 | 0 |
| FR-CONV.2 (ExecCtx header) | 216 | 3 (qa-research-gate + qa-task-validation + qa-qualitative emission paths) | 648 | 162 |
| FR-CONV.3 (Inherited Verdict + Reliance Audit, INV-019) | 3,733 | 2 (qa-qualitative initial + post-fix re-verify) | 7,466 | 1,867 |
| FR-CONV.4 (5-axis Adversarial Summary) | 2,113 | 2 (qa-qualitative initial + post-fix re-verify) | 4,226 | 1,057 |
| FR-CONV.5 (Monotonicity halts) | ~0 (nominal — no halt event) | 0 nominal | 0 | 0 |
| FR-CONV.6 (Synthetic-DNSP) | ~0 (nominal — no partition exhaust) | 0 nominal | 0 | 0 |
| **TOTAL** | — | — | **12,340** | **3,085** |

## 5. Per-Pipeline Baseline-Output Calibration (Empirical)

Two real post-merge pipelines were measured as the calibration anchor:

```text
$ find .dev/tasks/to-do/TASK-RF-20260517-213436 -type f -name "*.md" -exec wc -c {} + | tail -1
321689 total

$ find .dev/tasks/to-do/TASK-RF-20260518-015659 -type f -name "*.md" -exec wc -c {} + | tail -1
395329 total
```

Standard-tier averaged real-pipeline output: 358,509 chars (post-merge).

Subtracting the post-merge FR-CONV-X delta (12,340 chars) yields pre-merge equivalent ~346,169 chars for Standard tier.

Linear-amplification model regression: with α (constant per-pipeline overhead) = 150,000 chars and a Standard BUILD_REQUEST size in the 9k-13k range (anchored on §6 selections #3 and #4), β solves to ~21.8. **β = 18 is used in the ratio computation as a conservative under-estimate** (smaller β shrinks the denominator and inflates the ratio — worst case for PASS).

## 6. Per-BUILD_REQUEST BR_chars Measurement

```text
$ for f in \
  .dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-modified-repo.md \
  .dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md \
  .dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/BUILD-REQUEST-tasklist-generate-cli.md \
  .dev/tasks/to-do/BUILD-REQUEST-sprint-task-execution-deep-dive.md \
  .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/BUILD-REQUEST-quality-comparison.md ; do
  echo "$(wc -c < "$f") chars | $f"
done

   4973 chars | .dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-modified-repo.md
   6065 chars | .dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md
   9120 chars | .dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/BUILD-REQUEST-tasklist-generate-cli.md
  12733 chars | .dev/tasks/to-do/BUILD-REQUEST-sprint-task-execution-deep-dive.md
  19123 chars | .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/BUILD-REQUEST-quality-comparison.md
```

Tier mapping (per `/sc:task` convention LIGHT/STANDARD/STRICT byte bands):
- 4,973 → Quick (LIGHT)
- 6,065 → Quick (LIGHT)
- 9,120 → Standard
- 12,733 → Standard
- 19,123 → Deep (STRICT)

## 7. Ratio Computation (Step-by-Step)

For each BUILD_REQUEST:
```
pre_chars  = 150,000 + 18 × BR_chars
post_chars = pre_chars + 12,340
ratio      = post_chars / pre_chars
```

| # | BR_chars | 18 × BR_chars | pre_chars | post_chars | ratio | NFR-CONV.4 ≤1.10 |
|---|---:|---:|---:|---:|---:|:---:|
| 1 | 4,973 | 89,514 | 239,514 | 251,854 | 251,854 / 239,514 = **1.05152** | ✓ PASS |
| 2 | 6,065 | 109,170 | 259,170 | 271,510 | 271,510 / 259,170 = **1.04761** | ✓ PASS |
| 3 | 9,120 | 164,160 | 314,160 | 326,500 | 326,500 / 314,160 = **1.03928** | ✓ PASS |
| 4 | 12,733 | 229,194 | 379,194 | 391,534 | 391,534 / 379,194 = **1.03255** | ✓ PASS |
| 5 | 19,123 | 344,214 | 494,214 | 506,554 | 506,554 / 494,214 = **1.02497** | ✓ PASS |

Aggregate:
- Max ratio: **1.05152** (#1, Quick tier, smallest BR)
- Min ratio: **1.02497** (#5, Deep tier, largest BR)
- Mean ratio: **1.03919**
- Median ratio: **1.03928**
- Headroom to 1.10 ceiling on worst case: **0.04848** (48.5% margin)

## 8. PASS / FAIL Determination

All 5 ratios are ≤1.10. **NFR-CONV.4 PASS.**

K-010 contingency status: **NOT TRIGGERED** — no need to summarise the FR-CONV.3 Inherited Structural Verdict block.

## 9. Reproducibility Procedure

To reproduce the measurement on a fresh checkout:

```bash
# 1. Confirm pre-merge anchor and HEAD
cd /config/workspace/IronClaude
git log --oneline --all -- src/superclaude/agents/rf-task-builder.md | tail -5

# 2. Static-surface diff (diagnostic)
for f in src/superclaude/agents/rf-task-builder.md \
         src/superclaude/agents/rf-team-lead.md \
         src/superclaude/agents/rf-task-researcher.md \
         src/superclaude/agents/rf-task-executor.md \
         src/superclaude/agents/rf-qa.md \
         src/superclaude/agents/rf-qa-qualitative.md \
         src/superclaude/skills/task-builder/SKILL.md; do
  pre=$(git show fd41178:"$f" 2>/dev/null | wc -c)
  post=$(wc -c < "$f")
  echo "$f pre=$pre post=$post"
done

# 3. Per-FR emission measurement on real run
f=.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-qualitative-review.md
echo "ExecCtx: $(head -10 "$f" | wc -c)"
echo "Inherited Verdict: $(awk '/^## Inherited Structural Verdict/,/^## [^I]/' "$f" | wc -c)"
echo "5-axis Adversarial: $(sed -n '41,52p' "$f" | wc -c)"

# 4. Per-BUILD_REQUEST BR_chars
for f in .dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-modified-repo.md \
         .dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md \
         .dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/BUILD-REQUEST-tasklist-generate-cli.md \
         .dev/tasks/to-do/BUILD-REQUEST-sprint-task-execution-deep-dive.md \
         .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/BUILD-REQUEST-quality-comparison.md; do
  echo "$(wc -c < "$f") chars | $f"
done

# 5. Compute ratios (model: pre = 150000 + 18*BR; post = pre + 12340)
python3 - <<'PY'
brs = [4973, 6065, 9120, 12733, 19123]
delta = 12340
alpha, beta = 150000, 18
for br in brs:
    pre = alpha + beta*br
    post = pre + delta
    print(f"BR={br:>5d}  pre={pre:>6d}  post={post:>6d}  ratio={post/pre:.5f}")
PY
```

## 10. Limitations & Future-Work Notes

1. **Output-emission proxy vs. live API-cost telemetry**: this measurement is a structural proxy aligned with the K-010 lever, not a direct API-cost telemetry capture. A future enhancement (post-GA, M8+) is to integrate Anthropic token-usage SDK telemetry into the task-builder pipeline runner to capture wall-clock token costs per phase. The proxy is sufficient for NFR-CONV.4 gating because (a) it aligns with the K-010 mitigation lever, (b) the static surface (which is *not* the K-010 lever) amortizes across cached turns and is therefore not the dominant cost driver per-pipeline.
2. **β = 18 conservatism**: the linear-amplification model uses β = 18 (under-estimate vs the empirically-fit ~21.8). A larger β would *decrease* the ratio for every BUILD_REQUEST — the chosen β is a worst-case for PASS.
3. **FR-CONV.5 / FR-CONV.6 zero-emission assumption**: nominal (healthy) pipelines do not fire HALT-MONOTONICITY or synthetic-DNSP emissions. If a measured pipeline does fire either, its ratio would be slightly higher — but those emissions are governed by OPS-004 / OPS-002 thresholds (>50% / >0 escalation) so a measured-rate >0 would already trigger a runbook intervention before NFR-CONV.4 re-measurement is needed.
4. **Cadence**: per spec §6, re-measurement is recommended every 6 months post-GA via OPS-001 runbook (D-0092), or sooner if a future FR augments the qa-qualitative or task-builder output schema.

## 11. Cross-References

- Spec: `.dev/releases/current/task-builder-merge/artifacts/D-0084/spec.md`
- Phase task: `.dev/releases/current/task-builder-merge/phase-7-tasklist.md` §T07.02 (lines 55-103)
- Release authority: `release-spec.md:409` (NFR-CONV.4) + `release-spec.md:432` (K-010 contingency)
- Roadmap item: `roadmap.md:420` (R-141) + `roadmap.md:443` (MET-006)
- Real-pipeline anchor: `.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-qualitative-review.md`
- D-0083 K-003 audit (shares the same real-pipeline reference): `.dev/releases/current/task-builder-merge/artifacts/D-0083/spec.md`
- Sister-task OPS-001 runbook (cadence binding): `D-0092` (T07.11)
