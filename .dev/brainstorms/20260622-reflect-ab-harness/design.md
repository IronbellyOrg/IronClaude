---
topic: "Compare skill-mode (inference) vs CLI (fan-out) reflect POST-gate on a ground-truthed sample"
domain: process
strategy: systematic
created: "2026-06-22"
status: design
---

# Reflect A/B Harness — Experiment Design

## 1. The question

When `task-builder`'s default `reflect_post_mode: skill` gate runs, does the nested reflect
invocation **fan out a real reviewer ensemble**, or **degrade to a single-agent / hand-rolled
fixture** (per memory `reference_subagent_cannot_nest_skill_fanout`)? And **regardless of
fan-out, how good is the audit** — measured against known ground truth — compared to the CLI
(`superclaude reflect run`) path, which always fans out via a `claude --print` subprocess?

Two axes:
- **Between methods:** inference (skill/in-session) vs CLI (subprocess).
- **Within a method:** run-to-run consistency across 5 runs of the same method on the same sample.

## 2. The decisive design choice — a GROUND-TRUTHED sample

You cannot score audit *quality* by comparing runs only to each other (that measures
consistency, not correctness). The sample must contain a **known, planted set of deviations**
recorded in a hidden `ground-truth.yaml`. Each reflect run is then scored on precision/recall
against that gold standard. This is what makes "quality of the inference pipeline, regardless
of fan-out" measurable.

### Sample: a 10-file throwaway mini-package with planted deviations

Lives at `<EXP>/sample/` (EXP = `/config/workspace/IronClaude/.dev/experiments/reflect-ab/`),
built + executed by `/task-builder` + `/task`, then **committed and frozen** so every gate run
audits byte-identical input.

| # | File | Planted content (ground truth) | Expected reflect class |
|---|------|-------------------------------|------------------------|
| 1 | `calc/core.py` | `divide()` returns wrong value for 0-divisor, contradicting its docstring AND breaking test_core | **Regression** (HIGH) |
| 2 | `calc/stats.py` | extra `variance()` fn not in any tasklist item, no rationale | **Drift** |
| 3 | `calc/__init__.py` | exports a symbol `percentile` that does not exist (cross-file interaction) | **Regression** (import error) |
| 4 | `tests/test_core.py` | a test that now FAILS because of file #1 (feeds the verification triangle) | (evidence for #1) |
| 5 | `tests/test_stats.py` | passing tests | clean (control) |
| 6 | `config/settings.yaml` | `max_workers` changed 4→16 WITH an inline `# rationale:` comment | **Necessary** |
| 7 | `docs/api.md` | cites "§Limits" section that does not exist (dangling ref) + describes behavior the code contradicts | **Drift** + citation-accuracy probe |
| 8 | `docs/changelog.md` | documents a feature the tasklist's "Authorized expansion" item explicitly approved | **Authorized** |
| 9 | `cli.py` | silent default flag flip (`--verbose` now default-on), unmapped | **Drift** |
| 10 | `README.md` | accurate overview | clean (control / false-positive bait) |

Planted total: 1–2 Regression, 3 Drift, 1 Necessary, 1 Authorized, + 3 edge cases (failing
test, dangling citation, cross-file import). A correct audit MUST block promotion (the
regression), classify ≥4/6 deviations correctly, and NOT flag the 2 clean controls.

`ground-truth.yaml` (NOT placed where reflect reads it — kept at `<EXP>/ground-truth.yaml`,
outside the sample tree) enumerates `{id, file, line, class, severity, detect_signal}` per plant.

### Re-runnable seam (verified against the engine)
- `_resolve_base` precedence is `--base` → frontmatter `start_commit` → `merge-base` (config.py:81).
- Reflect diffs **BASE vs working tree** and **reuses the same base every re-audit** (runner.py:348/554).
- ⇒ Commit the executed sample on branch `exp/reflect-ab`; record `start_commit` = the commit
  *before* the sample work. Every gate run (any method, any workspace) audits the identical
  `start_commit..sample` delta. Run each in its own `git worktree` for full isolation.
- All measurement runs use **`--no-promote --no-fix`**: pure audit, no mutation, no terminal
  promote — so the sample stays pristine and the 5 runs are independent.

## 3. The three arms

| Arm | Invocation (per run) | What it exercises |
|-----|----------------------|-------------------|
| **Diagnostic (1×)** | `/task` top-level on the skill-mode-gate task | Does the *nested* POST subagent fan out or degrade? (the HD-1 question) |
| **Inference (5×)** | `/sc:reflect --mode post --base <start_commit> --tasklist <task> --depth deep --no-promote` (in-session skill) | Skill-path audit quality + run-to-run consistency |
| **CLI (5×)** | `superclaude reflect run <task> --base <start_commit> --depth deep --no-promote --no-fix` (subprocess) | Subprocess fan-out audit quality + consistency |

**Independence note (records a real limitation):** 5 inference runs in one session carry context
between runs (later runs "remember" earlier findings). The scoring framework's consistency index
will *detect* this (suspiciously high overlap). For maximum rigor, run each inference run in a
fresh session/worktree; the convenience default is sequential-in-session with the caveat logged.
CLI runs are naturally context-independent (fresh subprocess each time).

## 4. Comparable output: every run fills the SAME report template

See `report-template.md`. Each run (both methods) emits `<run-dir>/run-report.md` with identical
fields (tier, fan-out + reviewer-card count, deviations table, citation accuracy, verdict, cost),
plus its raw `return-contract.yaml`. The scoring subagent consumes these uniformly.

## 5. Scoring framework

See `scoring-framework.md`. Nine metric groups (G1–G9) scored against `ground-truth.yaml` and
across runs, producing a **matrix** (runs × metrics) and a **scorecard** (per-method mean±stddev,
cli−inference delta, within-method consistency index, headline verdict).

## 6. Risks / mitigations

- **Executor "fixes" the planted bugs.** Mitigation: the task items specify the flawed output
  verbatim as the deliverable ("implement divide() that returns 0 for divide-by-zero — DO NOT
  guard"), and the skill-mode QA is set to NOT auto-fix the planted issues; the build prompt
  verifies the plants survived via a post-execution `ground-truth` checksum before freezing.
- **Degrade-to-fixture is invisible.** Mitigation: G1 records reviewer-card count + tier; a
  "fanned out" run has ≥2 reviewer cards on disk, a degraded one has none.
- **Sample contamination across runs.** Mitigation: `--no-fix --no-promote` + one worktree per run.
- **Promotion fires and moves the task.** Mitigation: `--no-promote` everywhere except a final
  optional confirm run.
