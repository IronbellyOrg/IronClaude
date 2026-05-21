# cliEval suite manifests — naming convention

**Source-of-truth ADR:** [`decisions.md` §"DOC-OQ6 Closure"](../../../../../.dev/releases/current/cliEval/decisions.md)
**Roadmap row:** DOC-OQ6 / R-107 (open question OQ-6).
**Status:** Naming convention ratified 2026-05-20; `quick.yaml` recorded as a deferred follow-up.

This directory is the on-disk home for cliEval **suite manifests** —
the YAML files that `superclaude eval` reads to decide which evals
exist, what capabilities they require, and how their bodies are
shaped. Every file added here MUST follow the rules below or the
loader will reject it before any filesystem write happens (FR-SCH1 /
T01.04).

## What lives in this directory

| File                  | Purpose                                                                                  | Loader treatment |
|-----------------------|------------------------------------------------------------------------------------------|------------------|
| `suite.schema.json`   | JSON Schema (Draft 2020-12) that every `*.yaml` manifest validates against (DM-011).     | Excluded from the suite glob (`*.yaml` only). |
| `real.yaml`           | The 15-eval real-world suite (E1..E15) — v1's sole shipped suite (frozen at T05.01).     | Discovered by `discover_suite_manifests`. |
| `__init__.py`         | Exports `SCHEMA_PATH`. Not a manifest.                                                   | Ignored by the glob. |
| `<other>.yaml`        | Any future suite manifest authored under the naming rules in §"Filename rules".          | Discovered alongside `real.yaml`. |
| `*_callbacks.py`      | Optional sibling Python module exporting D-4 YAML-callback escape-hatch functions.       | Imported lazily by suites that name `callback:` entries; not a manifest. |

Anything else placed here — fixture files, scratch outputs, in-flight
drafts with a `.draft` or `.tmp` suffix — is ignored by the loader
glob (`suites_dir.glob("*.yaml")` at `commands.py:606`).

## Filename rules

A new suite manifest MUST satisfy **all** of the following:

1. **Extension is exactly `.yaml`** (lower-case). The loader glob is
   `*.yaml`; `*.yml`, `*.YAML`, and `*.json` are silently invisible
   to `eval list` / `eval describe` / `eval run --suite`. This is a
   deliberate one-spelling rule — see `commands.py:591-606`
   (`discover_suite_manifests`) and the design-spec §5 manifest
   contract.
2. **Stem is `[a-z][a-z0-9_]*`** — i.e. `snake_case`, lower-case
   alphanumeric plus underscore, starting with a letter. Examples
   that pass: `real.yaml`, `quick.yaml`, `mcp_only.yaml`,
   `freshness_followup.yaml`. Examples that FAIL: `Real.yaml`
   (upper-case), `real-suite.yaml` (hyphen), `1quick.yaml`
   (leading digit), `real.suite.yaml` (extra dot).
3. **Stem MUST equal the manifest `name:` field.** The loader's
   `--suite <token>` resolution at `commands.py:1008-1044` looks up
   matches by *(a)* direct path, *(b)* filename stem
   (`suites_dir / f"{token}.yaml"`), *(c)* schema-validated `name`.
   Rules (b) and (c) collapse to the same lookup only when stem ==
   `name`. Suites that mismatch still resolve via rule (c), but the
   `eval list` output prints the schema `name`, while operators
   typically reach for the stem — keeping them identical is the
   single rule that prevents the "the file is called `foo.yaml` but
   `--suite foo` errors out" trap.
4. **Stem MUST be globally unique within this directory.** The glob
   is deterministically sorted, but two manifests with the same stem
   cannot coexist on a case-insensitive filesystem. The schema
   `name:` field is also unique by convention (no enforcement at the
   schema layer; the precedent is "one manifest per suite").
5. **Reserved stems:** `suite` (clashes with `suite.schema.json`
   semantics in operator parlance) and any stem starting with `_`
   (would shadow the `__init__.py` convention). Neither is loader-
   enforced; both are convention-only.

The loader emits no rename-on-rejection diagnostic — a misnamed file
is simply not discovered. `eval doctor` (T01.13) will surface the
mismatch via `eval list` rendering an empty / unexpected count.

## Authoring checklist (when adding a new suite)

1. Pick a `snake_case` stem that satisfies §"Filename rules" §1-§5.
2. Write `<stem>.yaml` with a top-level `name:` field set to the
   stem.
3. Validate against the schema:
   ```bash
   uv run superclaude eval describe --suite <stem>
   ```
   A schema violation or eval-id regex rejection (FR-SCH2) raises
   before any filesystem write (NFR-SEC1 invariant).
4. If the suite carries D-4 callbacks, drop a sibling
   `<stem>_callbacks.py` next to the manifest and reference its
   symbols via `callback:` entries inside the YAML.
5. Update the suite inventory in this README's "What lives in this
   directory" table.

## Planned follow-up — `quick.yaml`

A second built-in suite, `quick.yaml`, is **planned but not shipped
in v1**. The plan was first surfaced in `roadmap.md` row 339
(R6 risk mitigation: *"--eval subset documented; future
suites/quick.yaml planned per OQ-6; perf budget tracked in M3
NFR-PERF3"*) and is recorded here as the canonical follow-up for
OQ-6.

### Why it's deferred (out of v1 scope)

The v1 eval roster (E1..E15) was frozen at T05.01 (OQ-2 resolution);
adding a curated `quick` subset before the full `real` suite has
landed and proven stable would (a) re-open the frozen set, (b) split
maintenance attention across two manifests with no operator
demand-signal yet, and (c) blur the SC2 / SC4 coverage and LOC
budgets recorded against `real.yaml` only. The `--eval <id>`
filter on `superclaude eval run` is sufficient as the v1 "subset"
escape hatch (see FR-CLI1 flag table).

### Intended shape (for the post-v1 follow-up)

- **Stem / `name:`:** `quick`.
- **Filename:** `quick.yaml` in this directory.
- **Roster:** a curated 3-5 eval subset of `real.yaml` covering the
  PostToolUse Read async path (E9) and one matcher branch each from
  the Edit / Write / serena trio (E6 / E7 / E8) — biased toward
  evals that pass on every host without `--no-mcp`. Final roster
  selected by the suite owner at follow-up time.
- **Acceptance signal:** total wall-clock budget < 90s on a clean
  Linux host (≈1/8 of `real.yaml`'s 12-minute walltime when
  `--parallel 8` is in effect; the 10-minute adoption ceiling from
  R6 frames the budget). This is a budget for the suite owner, not
  a loader-enforced gate.
- **Schema:** no changes required. `quick.yaml` validates against
  the same `suite.schema.json` as `real.yaml`; it inherits the same
  defaults / required_binaries / optional_capabilities surface.

### What's NOT in scope for the follow-up

- A second `quick.schema.json`. The schema is suite-agnostic; one
  schema file serves all manifests.
- Loader changes. The `*.yaml` glob already discovers `quick.yaml`
  on the day it lands.
- A new `--suite quick` CLI flag. The existing `--suite <token>`
  resolution at `commands.py:1008-1044` resolves `quick` to
  `quick.yaml` by filename stem (rule (b)) with zero CLI changes.

### Trigger to land it

The follow-up is unblocked when **either** of the following
materialises:

- A maintainer demand-signal: an explicit ask in tasklists / PR
  reviews for a sub-minute smoke suite that the `--eval <id>`
  filter does not address ergonomically.
- A measurement-driven case: post-v1 `real.yaml` walltime
  consistently exceeds the R6 10-minute adoption ceiling on the
  reference hardware described in NFR-PERF3 — at which point a
  curated `quick` becomes the documented "fast loop" path and
  `real` becomes the "full coverage" path.

Until then, `quick.yaml` is a documented intent, not a backlog
item. Reopening the decision requires citing this README and the
DOC-OQ6 closure in `decisions.md`; no new ADR is needed for the
follow-up itself (the contract above is the spec).

## Cross-references

- **DOC-OQ6 / R-107 (roadmap row 351):** the M6 deliverable that
  this README satisfies. The roadmap AC reads *"cli/eval/suites/
  README.md records naming convention; `quick.yaml` plan recorded
  as follow-up"* — both halves are covered by §"Filename rules"
  and §"Planned follow-up — `quick.yaml`" respectively.
- **OQ-6 (roadmap row 332, M5 Open Questions):** *"Suite filename
  convention beyond `real.yaml` (e.g., quick subset)"*. Closed by
  this README and the `decisions.md` DOC-OQ6 closure section;
  `signed_off_by: RyanW` lands at T06.09 alongside the rest of
  the SC5 OQ ledger.
- **`commands.py:591-606`** — `discover_suite_manifests` glob (rule
  §1 enforcement, by exclusion).
- **`commands.py:1008-1044`** — `resolve_suite_manifest` precedence
  (rule §3 rationale).
- **`suite.schema.json`** — `name:` field contract (rule §3 second
  half).
- **`roadmap.md` row 339 (R6 mitigation):** original surfacing of
  the `quick.yaml` plan.
- **OQ-2 (T05.01) §"OQ-2 Resolution" in `decisions.md`:** authority
  for the E1..E15 freeze that defers `quick.yaml` out of v1.
