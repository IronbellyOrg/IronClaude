# D-0108 — DOC-OQ6 suite naming convention + `quick.yaml` follow-up spec

**Task:** T06.04 (Phase 6, Roadmap DOC-OQ6 / R-107)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## DOC-OQ6 contract

Roadmap row 351 (DOC-OQ6 / R-107) requires:

> `cli/eval/suites/README.md` records naming convention; `quick.yaml`
> plan recorded as follow-up.

The authoritative satisfaction site is the new file `src/superclaude/cli/eval/suites/README.md`, with a complementary ADR-log entry at `.dev/releases/current/cliEval/decisions.md` §"DOC-OQ6 Closure" (R8 revision). The README is the source-of-truth contract that future suite authors read; the decisions.md section is the cross-referenced ADR entry that closes OQ-6 in the OPS-001 §B table notes (R8 update line).

## Naming-convention summary

| Rule | Value |
|---|---|
| **Extension** | Exactly `.yaml` (lower-case). `*.yml`, `*.YAML`, `*.json` are invisible to the loader glob. |
| **Stem charset** | `[a-z][a-z0-9_]*` — `snake_case`, alphanumeric + underscore, leading lower-case letter. |
| **Stem ↔ `name:` field** | Stem MUST equal the manifest `name:` field so `--suite <token>` resolves via filename-stem lookup (rule 2 of `resolve_suite_manifest`). |
| **Stem uniqueness** | Globally unique within `src/superclaude/cli/eval/suites/`. |
| **Reserved stems** | `suite` (clashes with `suite.schema.json` semantics) and any leading-underscore stem (shadow of `__init__.py`). |
| **Loader behaviour encoded** | `commands.py:591-606` (`discover_suite_manifests`, `*.yaml` glob, sorted by filename) and `commands.py:1008-1044` (`resolve_suite_manifest`, precedence path / stem / `name:`). |

The convention encodes already-shipped loader behaviour; no code changes accompany this ADR (the README is a forward-looking guard against silent loader-miss surprises for any future suite author).

## `quick.yaml` follow-up summary

| Field | Value |
|---|---|
| **Status** | DEFERRED — documented intent, not a backlog item. |
| **Why deferred** | v1 eval roster (E1..E15) frozen at T05.01 (OQ-2 resolution); no operator demand-signal for a curated subset yet; `--eval <id>` filter on `eval run` is sufficient v1 escape hatch (FR-CLI1). |
| **Intended stem / `name:`** | `quick`. |
| **Intended roster** | Curated 3-5 eval subset of `real.yaml` (e.g. E9 PostToolUse Read async + one each of E6/E7/E8 matcher trio); final selection by suite owner at follow-up time. |
| **Acceptance signal** | Total walltime < 90s on a clean Linux host at `--parallel 8` (≈1/8 of `real.yaml` 12-minute budget; bounded by R6 10-minute adoption ceiling). |
| **Schema impact** | None — `quick.yaml` validates against the same `suite.schema.json` as `real.yaml`. |
| **CLI impact** | None — existing `--suite <token>` resolution at `commands.py:1008-1044` resolves `quick` to `quick.yaml` by stem with zero CLI changes. |
| **Trigger conditions** | Either (a) a maintainer demand-signal for sub-minute smoke runs not addressed ergonomically by `--eval <id>`, OR (b) measurement-driven case: `real.yaml` walltime consistently > R6 10-minute adoption ceiling on reference hardware (NFR-PERF3). |
| **Reopening cost** | Zero — this README + the decisions.md DOC-OQ6 closure are the spec; no fresh ADR required. |

## OQ-6 resolution

| OQ | Prior status | New status | `resolution:` text |
|----|--------------|------------|--------------------|
| OQ-6 | OPEN (carried from M5 Open Questions table, roadmap row 332) | **RESOLVED — 2026-05-20** | Suite filename convention ratified at `src/superclaude/cli/eval/suites/README.md` (§"Filename rules"). `*.yaml` lower-case extension; `snake_case` stem matching `[a-z][a-z0-9_]*`; stem MUST equal manifest `name:` field; stem unique per directory; reserved stems `suite` and `_`-prefixed. `quick.yaml` is recorded as a deferred follow-up in the same README (§"Planned follow-up — `quick.yaml`") with shape, scope-exclusions, and trigger conditions documented; no v1 work, no schema changes, no loader changes required. |

OQ-6 was originally enumerated against M5 (roadmap row 332, M5 Open Questions). T06.04 closes it per the M6 DOC-OQ6 requirement (roadmap row 351). The SC5 OQ-1..OQ-10 ledger (T06.09) inherits this resolution verbatim.

## Acceptance-criteria → site map (T06.04)

| AC bullet (T06.04) | Where satisfied |
|--------------------|-----------------|
| File `src/superclaude/cli/eval/suites/README.md` documents the suite filename rules (alphanumeric, snake_case, `.yaml`). | `src/superclaude/cli/eval/suites/README.md` §"Filename rules" (rules 1-5). |
| README records the `quick.yaml` follow-up plan as a planned follow-up. | `src/superclaude/cli/eval/suites/README.md` §"Planned follow-up — `quick.yaml`" (with deferral rationale, intended shape, scope-exclusions, trigger conditions). |
| decisions.md DOC-OQ6 entry status changes to `resolved`. | `decisions.md` §R8 revision-log entry + §"DOC-OQ6 Closure" §"Closure of OQ-6" (`Resolution status: RESOLVED — 2026-05-20`) + OPS-001 §B "Update (R8 ... T06.04)" line noting OQ-6's flip. |
| `TASKLIST_ROOT/artifacts/D-0108/spec.md` records the naming convention summary. | This file. |

## Out of scope for T06.04

- Authoring `quick.yaml`. The deferral is recorded; the body lands when one of the documented trigger conditions materialises.
- Loader changes. The `*.yaml` glob + stem-resolution precedence are already on disk at `commands.py:591-606,1008-1044`; the README documents them, it does not modify them.
- Schema edits to `suite.schema.json`. The schema is suite-agnostic; the convention is layered on top, not into the schema.
- Editing `roadmap.md` or `.roadmap-state.json` — out of scope for DOC-OQ6 row 351.
- Authoring follow-up evals to fill a `quick.yaml` roster — those land with the follow-up itself, not here.
- Renaming `real.yaml`. The existing manifest already satisfies the convention (stem `real` matches `[a-z][a-z0-9_]*`; `name:` field is `real`); no migration required.
