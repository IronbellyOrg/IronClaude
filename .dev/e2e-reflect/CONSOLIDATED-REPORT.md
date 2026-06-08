# E2E Reflect-Gate Test — Consolidated Report

**Date:** 2026-06-04 · **Feature:** PR #138 (reflect gates in `/task-builder` + `/sc:tasklist`)
**Agents:** 9 parallel Sonnet (6 generation + 3 sprint) · **Isolation:** 0 tracked files modified (all output sandboxed)

## Verdict

The reflect-gate **contracts and downstream compatibility are validated**. Every consumer
(`/task` HALT, `/sc:task` exec, `superclaude sprint run` ingest/scan) handles the new surfaces.
**3 actionable findings** + **1 harness limitation** surfaced. No blocker for the feature itself.

## Scoreboard

| # | Agent | Facet | Result |
|---|-------|-------|--------|
| 1 | tb-1 | PRE gate spec-backed → `reflect_pre: pass`; POST HALT | PASS¹ |
| 2 | tb-2 | specless degrade → `verdict: skipped (no-spec)`; POST still templated | PASS¹ |
| 3 | tb-3 | TCS override O2 (refactor→deep), O4 (POST never quick) | PASS¹ |
| 4 | tl-1 | Stage 10.5 fan-out + terminal reflect task + index column | PARTIAL |
| 5 | tl-2 | `--no-reflect` suppresses both gates | PASS |
| 6 | tl-3 | per-phase COMPLEXITY_SCORE override (deep/tier2 floor) | PASS |
| 7 | sprint-1 | sprint ingest/scan of reflect-gated bundle | PARTIAL |
| 8 | sprint-2 | sprint ingest/scan of `--no-reflect` bundle | PASS |
| 9 | sprint-3 | sprint ingest/scan of STRICT/CPO bundle | PASS |

¹ POST-gate HALT verified **live** on real `/task`; PRE-gate *emission* validated on an agent-authored
spec-faithful fixture (see Harness Limitation).

## What was genuinely validated (live)

- **POST-gate HALT contract** — real `/task` execution did the sandbox work, then **stopped** at the
  POST reflect item (`reflect_post: PENDING`, surfaced `/sc:reflect`, never inline, Done not flipped). (tb-1/2/3)
- **Deterministic depth** — O2 forced `deep` on a `🔧 Refactor` task (tcs=18); O4 kept POST command `≥ standard`. (tb-3)
- **`--no-reflect` escape hatch** — clean suppression: no terminal task, no Stage 10.5 output, no `depth-map.yaml`,
  no `reflect_pre_summary`; sprint treats it as a normal bundle. (tl-2, sprint-2)
- **Per-phase COMPLEXITY override** — auth/migration phase `n_strict:3, n_cpo:3` → floored `deep`/`tier 2`;
  docs phase stayed `quick`. (tl-3)
- **Sprint compatibility** — `sprint run --dry-run` + bounded `--max-turns 0` scans ingested all 3 bundles and
  enumerated every task incl. the terminal `Post-Execution Reflection` task **without parse error**;
  `Never /sc:task` guard prose did not break the scanner. (sprint-1/2/3)

## Actionable findings

### F1 [HIGH] — sprint does not honor `Tier: EXEMPT` on the terminal reflect task
The feature templates the terminal reflect task as **Tier EXEMPT** (`SKILL.md:1050`, `phase-template.md:141`)
specifically so it is *not* auto-executed and remains a fresh-session, executor-disjoint handoff.
**sprint-1 observed that sprint's `TaskEntry` drops the Tier field entirely** — so in an *unbounded* real
`sprint run`, sprint would attempt to execute the terminal task's `/sc:reflect` spawn directive **as ordinary
phase work**, running reflect inside the sprint's own frame and defeating the executor-disjoint design.
→ **Confirm against a real generator bundle; if real, sprint must special-case the terminal reflect task
(skip/handoff on `Tier: EXEMPT` or on the `Post-Execution Reflection` heading) rather than execute it.**

### F2 [MED] — `verify-checkpoints` path doubling
sprint-1: `verify-checkpoints` resolved a doubled path
`.../bundle/.dev/e2e-reflect/tl-1/bundle/checkpoints/CP-P02-END.md` (found 1 / missing 1). Likely tied to a
repo-rooted relative checkpoint path joined onto the bundle root (possibly an artifact of the non-canonical
`--output .dev/e2e-reflect/...` location vs the canonical `.dev/releases/current/`). Not caused by the reflect
feature, but a real path-join smell to confirm.

### F3 [MED] — template guard hygiene (2 guards)
- **F3a** (tl-1): the terminal task's own negative guard `Never /sc:task` contains the literal `/sc:task`
  token → trips any strict "no `/sc:task` substring anywhere" scanner. Sprint tolerated it, but consider
  rephrasing (e.g. "never the sc:task command") or asserting only on the spawn-directive line.
- **F3b** (tb-3): quoted-emoji `type: "🔧 Refactor"` — if the TCS S6 extractor doesn't normalize the quoted
  emoji value, `S6` reads 0 and O2 won't force `deep` (O4 still protects POST from `quick` only if applied
  independently at command emission). Add an emoji-quoted-`type` normalization + a unit test.

## Harness limitation (transparency)

The 3 `/task-builder` agents (and the `/sc:tasklist` agents to a lesser degree) **could not run the real
nested-subagent pipelines** from inside a background subagent: `/task-builder` spawns rf-analyst/rf-qa/reflect,
and `/sc:tasklist` spawns 2N validation + N pre-reflect agents. A background subagent cannot fan out its own
subagents, so those agents loaded the skills, authored **spec-faithful fixtures**, and verified the **executable
contracts** (/task HALT, /sc:task exec, sprint ingest) against them.

**Net:** the output *shapes* and the *consumers* are validated; the **live producers** (the PRE gate / Stage 10.5
actually emitting those surfaces during a real generation) were **not** exercised end-to-end. A true live test
must invoke `/task-builder` and `/sc:tasklist` from a **top-level session**, not a nested subagent.

## Follow-ups (recommended)

1. **F1** — decide the sprint × terminal-reflect-task contract; add a sprint scan rule for `Tier: EXEMPT` /
   `Post-Execution Reflection` tasks (highest value — it's the executor-disjoint guarantee under sprint).
2. **F3b** — emoji-quoted `type:` normalization + test in the TCS S6 extractor.
3. **F3a** — reword the terminal-task `/sc:task` negative guard.
4. **F2** — confirm/fix the checkpoint path doubling.
5. Re-run a **top-level live** `/task-builder` + `/sc:tasklist` once (outside a subagent) to close the producer gap.
