# Blinding Protocol — Reflect A/B Harness

Three roles, strictly separated. The auditor must never share context with a knower.

| Role | Knows ground truth / objective? | Who |
|------|-------------------------------|-----|
| **Builder** | YES (it plants them) | Prompt 1 session |
| **Auditor** (runs the reflect gate) | **NO — fully blind** | Prompt 2A fresh chats (inference); the `claude --print` subprocess (cli) |
| **Scorer** | YES (it grades vs ground truth) | Prompt 2B / Prompt 3's scoring subagent |

## Why the two arms have different prompt shapes (this is the point, not an inconsistency)

- **CLI auditor** runs in a `claude --print` **subprocess** that does NOT inherit chat context. So the orchestrating session may know everything and still not leak into the audit. ⇒ Prompt 3 can be one prompt: run 5×, then spawn the scorer subagent.
- **Inference auditor** runs the skill **in the orchestrator's own session**. Anything that session has read (objective, plant table, ground truth, even the fan-out-watching report template) is in-context when reflect runs. ⇒ the inference run MUST be an isolated fresh chat containing ONLY the reflect command. The scorer is a SEPARATE chat. There is no blind one-prompt-runs-5×-in-session version; that structure is inherently leaked.

## Leak controls

1. **Auditor reads only:** `base.sha`, `task-path.txt` (a SHA and a path — neither reveals the objective). Never `design.md`, never `ground-truth.yaml`, never `scoring-framework.md`, never `report-template.md` (the template names `fanned_out`/`degraded_to_fixture` — a tell while reflect is in-session).
2. **All interpretation is post-hoc.** The auditor only produces raw reflect artifacts (`return-contract.yaml`, `REPORT.md`, `reviewer-cards/`). The scorer transcribes them into `run-report.md` AND grades — it is the only one that opens `ground-truth.yaml`. Knower ≠ grader.
3. **Builder leak-scan (Class-A control, Prompt 1).** Before freezing, fail the build if the task file or `sample/` contains experiment/meta language: `grep -riE 'experiment|ground.?truth|planted|reflect|inference|cli|drift|regression test|for testing|fan.?out'`. The task must read like a normal feature task; the sample like normal code.
4. **Realism rule (Class-A control).** Plants must be as subtle as production defects — no giveaway names/comments (`drift_helper`, `# intentional bug`). A plant a human reviewer would miss on a quick pass is the target difficulty.
5. **Neutral scoring.** The scorer emits metrics only (matrix + scorecard). It does NOT recommend flip-vs-keep or reference HD-1. The cross-method `comparison.md` is per-metric deltas only. The decision interpretation is a separate human step.
6. **Pre-registration.** Before any run, write `EXP/prereg.md` with the expected/hoped outcome and the decision rule. Post-hoc rationalization is then visible against it.

## Residual risks (named, not hidden)
- The task lives under `.dev/experiments/reflect-ab/` — a weak path-name tell to a blind auditor. It reveals nothing about ground truth or the objective; optionally place the task+sample under a neutral subdir (`EXP/wd/`) to remove even that.
- The inference fresh-chat runs still share one thing: the same model defaults. That's intended (we're testing the method, not the model).
- A maximally-rigorous variant runs the builder itself blind to which arm "should" win and has a third party verify plant subtlety; for an internal decision aid this is usually overkill.
