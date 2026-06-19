# Design Note — `--spec §22` reconciliation + Stage-7 P3 exhaust-point pin

**Created:** 2026-06-19 (Step 1.6). Binding sources: research/07 §2a-§2c, research/08 R-13, R-1.
All text below is copied VERBATIM from the research; no paraphrase. The em-dash `—` is preserved.

---

## (1) `--spec §22` bounded behavior-preserving edit (R-13 §2b)

**Anchor:** `SKILL.md` lines 49-57 (Input Contract; sits between `## Input Contract` at :47 and the
`---` separator at :59). Confirmed current lines 49/57 in anchor-map.md.

### EXACT verbatim CURRENT text to replace (lines 49-57)

```
You receive exactly one input: **the roadmap text**.

The roadmap may contain:

- Phases, milestones, versions, epics, bullets, paragraphs
- Requirements, features, risks, success metrics, constraints
- Vague items ("improve performance", "harden security")

Treat the roadmap as the **only source of truth**.
```

### EXACT verbatim REPLACEMENT text (behavior-preserving, research/07 §2b)

```
You receive one **required** input — **the roadmap text** — and may receive
**optional supplementary inputs** (`--spec <spec-path>`, or auto-wired
TDD/PRD paths from `.roadmap-state.json`; see §3.x Source Document
Enrichment and §4.1a/§4.4a).

The roadmap may contain:

- Phases, milestones, versions, epics, bullets, paragraphs
- Requirements, features, risks, success metrics, constraints
- Vague items ("improve performance", "harden security")

Treat the roadmap as the **primary source of truth** for task generation:
every task MUST trace to a roadmap item (R-### traceability). Supplementary
TDD/PRD inputs, when present, only **enrich** roadmap-derived tasks
(specificity, acceptance criteria, validation, deployment phases) and the
pre-reflect spec resolution (§10.5) — they never originate tasks that lack
a roadmap anchor. Without supplementary inputs, the generator works from
the roadmap alone (the baseline behavior described in §3.x).
```

**Behavior-change assertion:** this edit changes **NO flag, NO algorithm step, NO emitter, NO gate**.
It keeps the middle bullet list (lines 50-56) **verbatim** and rewrites only the opening sentence (49)
and the closing "only source of truth" sentence (57). It makes the already-true `--spec` behavior
(advertised at `:9`; implemented at `:169-182`, `:246-267`, `:1297-1308`, `:1466-1471`) self-consistent.

---

## (2) Residual removal-path Open Question — `needs_human_decision`, MUST-HALT (R-13 §2c)

The §2b reconciliation assumes intent = "keep `--spec` enrichment; fix the stale contract prose."
There is a second, materially different possibility the builder/executor CANNOT resolve from source
alone. This MUST be recorded as a HALTING Open Question (Step 7.2) and MUST NOT be auto-applied.

### VERBATIM Open Question text (research/07 §2c)

> **OPEN QUESTION (human decision required):** Does the maintainer instead want to **REMOVE
> `--spec`/source-document enrichment** to make the generator *truly* roadmap-only (honoring lines
> 49/57 as the intended contract)? That is a **behavior change** — it would delete §3.x (130-147),
> §4.1a (169-183), §4.1b (185+), §4.4a (246-267), §4.4b (269+), the Stage-7 Supplementary TDD
> Validation (1297-1308), the `--spec` thread in Stage 10.5 (1466-1471), and the
> `--spec`/`--tdd-file`/`--prd-file` flags from `argument-hint` (line 9) and the CLI. This is **out
> of P1-P5 scope** and **MUST NOT be auto-applied.**

**This build's applied default:** the bounded behavior-preserving edit (1) ONLY; **removal NOT applied**.
**Status:** PENDING (HALTS — do not auto-apply). Decision required from: maintainer.

---

## (3) Stage-7 P3 `escalation_ladder_exhaust_point` pin = `retry-1` (R-1)

**Binding (research/08 R-1):** Stage 7's ladder is a SINGLE retry — `SKILL.md:1310` verbatim:
*"Zero agent failures (if an agent fails, retry once before reporting error)."* Therefore the
conformant exhaust-point for a Stage-7 validation agent that fails after its one retry is **`retry-1`**
(the existing first member of the closed vocab `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2,
gap-fill-round-3}`). No vocabulary extension, no fork.

**Pinned `dedup_key` shape (2 elements):**

```
["<stage7_affected_range>", "retry-1"]
```

The 2nd element is the pinned `retry-1`. (If a future change adds a second Stage-7 retry, `retry-2` is
already available.) This keeps P3 conformant to the task-builder DM-003 contract verbatim.
