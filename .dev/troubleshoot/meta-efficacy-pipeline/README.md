# Troubleshoot-Efficacy Pipeline

A **re-runnable Workflow** that answers: *how much of our debug → task-build →
reflect → validate stack is theatre vs net value?* — then root-causes the
misses, derives **issue-agnostic** remediations, refactors **sc:troubleshoot
only**, and **proves** the refactor by rolling the PRD code back to the
pre-whack-a-mole commit and replaying the new pipeline against a fixed
ground-truth miss set (loop **≤ 3 rounds**).

> Built as an artifact only (per the operator's scope decision). Nothing is
> executed until you launch it. The live PRD resume run is unaffected.

## Run it

```text
Workflow({ scriptPath: ".dev/troubleshoot/meta-efficacy-pipeline/troubleshoot-efficacy.workflow.js" })
```

- Re-run: same `scriptPath`. Resume a killed run: add `resumeFromRunId: "<wf_…>"`.
- Watch live: `/workflows`.
- Final artifact: `.dev/troubleshoot/meta-efficacy-pipeline/EFFICACY-REPORT.md`
  (+ a worktree at `/tmp/prd-rollback-ac80f176`).

## Locked scope (your decisions, 2026-06-10)

| Decision | Setting |
|---|---|
| Deliverable | **Artifact only** (this Workflow + README) |
| Refactor target | **sc:troubleshoot only** (command + skill/protocol + its agents) |
| Validation loop | **≤ 3** refactor→replay rounds |
| Forensic grounding | **git history + `.dev` artifacts + this session's live-caught issues** |

## The phase DAG (max parallelization)

```
P1 Forensic Timeline ──(3 readers ∥)──► aggregate ► miss registry + THEATRE SCORECARD
        │
        ▼   (pipeline: each miss flows independently, NO barrier)
P2 Hypotheses (×2 ∥ per miss)  ─►  P3 Adversarial Merge (per miss) ─► validated root cause
        │
        ▼   (barrier: needs all per-miss causes)
P4 Systemic Synthesis ► 2–4 structural causes
        │
        ▼   (pipeline per cause)
P5 Generalized Remediation (×2 ∥ per cause) ─► adversarial merge ─► 1 issue-agnostic strategy
        │
        ▼
P6 Troubleshoot Refactor (+ would-have-caught matrix over M1..Mn)
        │
        ▼   (loop ≤ 3)
P7 Rollback Replay @ ac80f176 ─► coverage% vs ground truth ─► gaps ─► refine ─► replay …
        │
        ▼
EFFICACY-REPORT.md
```

Parallelism: P1 readers run together; P2→P3 use `pipeline()` so each miss's
hypotheses+merge run concurrently with every other miss's (wall-clock = slowest
single miss, not the sum); P5 parallelizes the two remediations per cause. P4
and P7 are the only barriers (synthesis needs all causes; replay is sequential
by round).

## Ground-truth miss registry (the replay oracle)

Embedded in the script as `GROUND_TRUTH`; P1 re-derives and may extend it.
Rollback target **`ac80f176`** = PRD state immediately before PR #151.

| ID | Miss | Surfaced by | Fix |
|----|------|-------------|-----|
| **M1** | PRD passed local paths to cloud-only `claude --file` → token crash | runtime (scope-discovery exit 1) | #151 `7601ad25` |
| **M2** | `_check_parallel_instructions` enforced on the sequential completion phase | runtime (build-task-file halt) | #154 `e97aa4fd` |
| **M3** | same regex matched Task-Log `Phase N - … Findings` headings; **unmasked by M2's fix** | runtime (next halt) | colon/heading fix (superseded) |
| **M4** | **theatre exemplar** — advisory fix applied to `gate_passed`, but runtime uses `_evaluate_gate`; verification tested the *unused* path → false green | runtime (still halted) | #158 `_evaluate_gate` |
| **M5** | `_check_verdict_field` rejected decorated verdicts (`## Verdict: ✅ PASS`, `- **Verdict:** ✅ **PASS**`) across ~5 QA gates | runtime (research-qa halt) | verdict branch |
| **M6** | resume step-ID mismatch (`research-qa` vs `qa-research-gate`) | runtime (CLI error) | uncommitted |

Recurring shapes the pipeline is built to expose: **(a)** fixes reasoned about
the symptom in isolation, never against an end-to-end run; **(b)** verification
targeted the artifact-under-design, not the executed path (M4); **(c)** fixing
gate X unmasks gate Y, no blast-radius analysis (M3); **(d)** per-instance fixes
never recognized the brittle-parser *class* (M5); **(e)** gates downstream of
the first failure are never *exercised* → bugs reveal strictly one-at-a-time.

## What each phase produces (all schema-validated)

- **P1** `miss registry` + `theatre_scorecard` (per review step: should-catch vs did-catch → theatre ratio).
- **P2/P3** per-miss: 2 hypotheses (process-design lens + epistemics lens) → adversarial-merged validated root cause.
- **P4** 2–4 systemic causes with the structural reason the pipeline is blind to each.
- **P5** one **issue-agnostic** remediation per cause (hard constraint: no PRD/parallel/verdict specifics; must show generality to ≥2 unrelated systems).
- **P6** concrete sc:troubleshoot refactor + a `would_have_caught` matrix (per miss: caught? by which mechanism? at which wave?).
- **P7** per round: `coverage_pct`, `caught[]`, `missed[]`, gap→needed-mechanism; loops ≤3, refining the refactor from gaps.
- **Final** `EFFICACY-REPORT.md` with the blunt bottom line: would the refactor have caught **all** of M1..Mn in one shot at `ac80f176` — and what is irreducibly un-catchable by *static* troubleshooting (and therefore needs a runtime/exercise mechanism).

## Design choices worth knowing

- **Adversarial merges are inline agents** implementing sc:adversarial Mode-A
  logic (steelman → score → merge → graft loser's best). This keeps the
  Workflow self-contained (no dependency on whether workflow-agents can invoke
  the `sc:adversarial` Skill). Swap to `workflow("sc:adversarial", …)` if you
  prefer the full skill.
- **Honesty guard built into P7**: a mechanism only "catches" a miss if the
  agent can name the concrete artifact/check that flags it — verified against
  the rolled-back code in the worktree. This is what prevents the report from
  being theatre about theatre.
- **The likely punchline** (hypothesis the run will test): several misses
  (M2/M5/M6 especially) are *only* discoverable by **exercising the runtime
  path**, so a purely-static troubleshoot refactor will hit a coverage ceiling
  — and the strongest generalized remediation is probably "the fix must produce
  an executable that drives the real path past the symptom," not more reading.
  P7's residual-gap analysis is designed to surface exactly that.

## Tuning knobs (edit the script)

- Loop bound: the `for (round 1..3)` in P7.
- Lenses / remediation angles: `LENSES` and the P5 `angle` array.
- Rollback target: `ROLLBACK_COMMIT`.
- Broaden refactor to the full chain (task-builder + reflect): relax the P6 prompt's "sc:troubleshoot ONLY" clause.
