# Falsifier Suite — `sc-reflect-protocol`

The falsifier suite contains cases that **must remain failable**. They are not regression tests for happy-path behavior; they probe the protocol's structural guarantees — heterogeneous reviewer ensemble (Khan ICML 2024 weak-judge-strong-debaters), blind calibration (disjoint-set rule), and the §11 hallucination contract — by feeding the skill fixtures specifically constructed to defeat them.

## Sufficiency contract (per spec §11.0)

The protocol claims that its three structural mechanisms (heterogeneous reviewer ensemble at Tier 2, blind calibration of every reviewer card, mandatory evidence-validator gate) are *sufficient* to defeat single-model representational bias when the inputs are well-formed. The falsifier suite is the **negative-space discipline** that makes this claim falsifiable: if any case here passes when it should fail, the sufficiency claim is empirically wrong and the protocol needs revision.

The §11.0 sufficiency claim is conditional on three gates being intact:

1. Reviewer ensemble seats are drawn from different model classes (Khan disjoint-set rule).
2. The calibrator's model class is disjoint from every reviewer's model class.
3. `evidence-validator` runs as the final gate on every Grounded citation.

If any gate degrades (e.g., `--no-evidence-validator`), the sufficiency claim is downgraded with explicit telemetry — the protocol does not silently pretend it still holds.

## Dual-state lifecycle (per spec §12.5 + W-A8 spec-panel fix)

Each falsifier case ships in one of two states:

| State | Status field | What it means | When it pass |
|-------|--------------|---------------|--------------|
| **Skeleton (v1.0, v1.x)** | `status: skeleton-pending-iteration-3-fixture` | Case file exists with `id`, `description`, and `expected_grader_emission`, but the fixture content (e.g., `fixtures/spec-with-deliberate-misclassification.md`) is a placeholder. | Pass when the grader's `falsifier_skeleton_present` assertion returns true (skeleton file exists AND parses AND has the byte-exact `skeleton-pending-iteration-3-fixture` status value). |
| **Active (iteration-3+)** | `status: active` | Fixture content authored; canonical assertion `convergence_score < 0.75 OR verdict == regression_present` is evaluated against an actual reflect run on the fixture. | Pass when the case has all canonical fields (`id`, `type`, `fixture`, `expected`, `assertion`) AND the canonical assertion holds when the eval runner executes the fixture. |

The grader returns the same boolean PASS/FAIL for both states — what differs is the underlying check. While skeleton-pending, the grader only verifies the structural contract. While active, the grader executes a fixture run and evaluates the actual runtime assertion.

## Grader handling

The `falsifier_skeleton_present` assertion (defined in `refs/grader-extensions.md` and implemented in `grader.py`) does the following:

1. Verify the case YAML exists at the expected path under `cases/falsifier-suite/`.
2. Verify it parses as valid YAML.
3. Read the `status` field.
4. If `status == "skeleton-pending-iteration-3-fixture"` → return PASS with evidence `"skeleton present (pending iteration-3 fixture)"`.
5. If `status == "active"` → verify the case has all canonical fields (`id`, `type`, `fixture`, `expected`, `assertion`). If yes → return PASS (the runtime convergence check is layered on top by the eval runner). If a required canonical field is missing → return FAIL.
6. Any other status value → return FAIL.

The grader also emits a `skeleton_present: true` telemetry row to `metrics.json` (per §15.1 schema) when in skeleton state, so dashboards can track when each case promotes to active.

## Iteration-3 promotion checklist

When iteration-3 follow-up work promotes a falsifier case from skeleton to active, the operator MUST:

1. Replace `status: skeleton-pending-iteration-3-fixture` with `status: active` in the case YAML.
2. Add the required canonical fields: `type`, `fixture` (pointing to the authored fixture content), `expected`, `assertion`.
3. Author the fixture content (e.g., flesh out `fixtures/spec-with-deliberate-misclassification.md` with the deliberately-misclassified deviation, or author the runtime fixture for `T2-judge-class-collision`).
4. Run `make reflect-eval` against the new active case to confirm the canonical assertion (`convergence_score < 0.75 OR verdict == regression_present`) actually triggers on the deliberately-broken input.
5. If the canonical assertion DOES NOT trigger (the protocol "passes" when it should fail), the falsifier has succeeded — file an incident, escalate the protocol revision, and DO NOT silently widen the assertion to make it pass.

## Cases in this suite (v1.0)

- **`T2-converges-on-wrong.yaml`** — Heterogeneous reviewer ensemble must NOT converge on a deliberately-wrong answer when fed a fixture with deliberate misclassification. Tests the ensemble-diversity guarantee.
- **`T2-judge-class-collision.yaml`** — Reviewer-seating algorithm must REFUSE to seat a reviewer whose model class collides with the calibrator's model class. Tests the Khan ICML 2024 disjoint-set rule enforcement.

Both ship as SKELETONS in v1.0; iteration-3 follow-up promotes them to active and authors the underlying fixture content. See `TASK-RF-20260527-043715-sc-reflect-rebuild` Follow-Up Items for the iteration-3 plan.
