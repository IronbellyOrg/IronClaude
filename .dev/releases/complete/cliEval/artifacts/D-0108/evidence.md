# D-0108 — Evidence

## Direct verification commands

```bash
# 1) Confirm README exists at the expected path
test -f src/superclaude/cli/eval/suites/README.md && echo OK

# 2) Confirm README §"Filename rules" header is present
grep -nE '^## Filename rules' src/superclaude/cli/eval/suites/README.md

# 3) Confirm README §"Planned follow-up — `quick.yaml`" header is present
grep -nE '^## Planned follow-up — `quick\.yaml`' src/superclaude/cli/eval/suites/README.md

# 4) Confirm DOC-OQ6 Closure section header in decisions.md
grep -nE '^## DOC-OQ6 Closure' .dev/releases/current/cliEval/decisions.md

# 5) Confirm OQ-6 closure status flip
grep -nE 'Resolution status:\s+RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md \
  | head -5

# 6) Confirm R8 revision-log entry recorded
grep -nE '^- R8 \(2026-05-20\): DOC-OQ6 closure' .dev/releases/current/cliEval/decisions.md

# 7) Confirm R8 update note in OPS-001 §B references OQ-6
grep -nE 'Update \(R8, 2026-05-20 — T06\.04\)' .dev/releases/current/cliEval/decisions.md

# 8) Confirm `real.yaml` already satisfies the convention
head -1 src/superclaude/cli/eval/suites/real.yaml
```

Expected: commands 1, 4, 6, 7 return `OK` / one match; commands 2, 3, 5 return one or more matches; command 8 prints `name: real`.

## Per-AC verification

| AC bullet (T06.04) | Verification step | Result |
|--------------------|-------------------|--------|
| File `src/superclaude/cli/eval/suites/README.md` documents the suite filename rules (alphanumeric, snake_case, `.yaml`). | `test -f` the path; `grep` for §"Filename rules"; inspect rules 1-5. | PASS — README exists; §"Filename rules" present; rules §1 (`.yaml`), §2 (`[a-z][a-z0-9_]*` snake_case), §3 (stem == `name:`), §4 (uniqueness), §5 (reserved stems) all enumerated. |
| README records the `quick.yaml` follow-up plan as a planned follow-up. | `grep` for §"Planned follow-up — `quick.yaml`"; inspect deferral rationale, intended shape, scope exclusions, trigger conditions. | PASS — §"Planned follow-up — `quick.yaml`" present with: (a) deferral rationale (OQ-2 freeze, no demand-signal, `--eval` as escape hatch), (b) intended shape (stem `quick`, 3-5 eval subset, <90s walltime, same schema), (c) what's NOT in scope (no second schema, no loader changes, no new CLI flag), (d) trigger conditions (maintainer demand-signal OR R6 walltime ceiling exceeded). |
| `decisions.md` DOC-OQ6 entry status changes to `resolved`. | `grep` for §"DOC-OQ6 Closure"; confirm Resolution status line reads `RESOLVED — 2026-05-20`; confirm R8 revision-log entry present; confirm R8 update note in §B OPS-001 names OQ-6's M5 provenance. | PASS — §"DOC-OQ6 Closure" present (line 694); Resolution status RESOLVED — 2026-05-20 (line 735); R8 entry in revision log (line 14); R8 update note in §B OPS-001 (line 493) records OQ-6's M5 provenance + RESOLVED status. |
| `TASKLIST_ROOT/artifacts/D-0108/spec.md` records the naming convention summary. | Confirm file exists with: DOC-OQ6 contract, naming-convention summary table, `quick.yaml` follow-up summary table, OQ-6 resolution table, AC → site map, out-of-scope list. | PASS — `artifacts/D-0108/spec.md` written this commit; structure mirrors D-0107/spec.md. |

## Loader-behaviour audit — what the convention encodes

The convention recorded in the README does not introduce new loader behaviour; it documents what the loader already does. Audit methodology:

```bash
# Sweep loader source for the glob pattern + resolution precedence
grep -nE 'suites_dir\.glob\(|resolve_suite_manifest\b|discover_suite_manifests\b' \
  src/superclaude/cli/eval/commands.py

# Sweep schema for the `name:` field constraint
grep -nE '"name"\s*:\s*\{|"required"\s*:\s*\[' \
  src/superclaude/cli/eval/suites/suite.schema.json
```

### Results (2026-05-20)

**Loader behaviour (`commands.py`).**

| Symbol | Line range | Behaviour |
|---|---|---|
| `discover_suite_manifests` | 591-606 | `suites_dir.glob("*.yaml")`, sorted by filename. Encoded as rule §1 in the README. |
| `resolve_suite_manifest` | 1008-1044 | Three-stage precedence: (1) direct path, (2) `<token>.yaml` filename-stem lookup at line ~1030-1032, (3) schema-validated `name` field. Rules (2) and (3) collapse to the same lookup when stem == `name:` — encoded as rule §3 in the README. |

Zero non-`*.yaml` glob patterns exist in the loader path. Zero alternate stems are accepted via case-folding. The convention encodes the loader, not the other way around.

**Schema behaviour (`suite.schema.json`).**

| Field | Constraint | Convention layer |
|---|---|---|
| `name` | `{"type": "string", "minLength": 1}` | Schema requires non-empty string; convention rule §2 narrows to `[a-z][a-z0-9_]*`. |
| `name` (uniqueness) | No uniqueness constraint at the schema layer. | Convention rule §4 narrows by directory uniqueness. |
| Reserved stems | None at the schema layer. | Convention rule §5 narrows to forbid `suite` and `_`-prefixed. |

The README's §"Filename rules" are convention-layered on top of the schema, not redundant with it. The schema-vs-convention split is recorded explicitly in `artifacts/D-0108/notes.md` §4.

**`real.yaml` conformance audit.**

```yaml
# src/superclaude/cli/eval/suites/real.yaml (line 1)
name: real
```

| Rule | `real.yaml` status |
|---|---|
| §1 (`.yaml` extension) | Satisfied. |
| §2 (`[a-z][a-z0-9_]*` stem) | Satisfied — stem `real` matches. |
| §3 (stem == `name:`) | Satisfied — `name: real` matches stem `real`. |
| §4 (unique stem) | Satisfied — only manifest in directory. |
| §5 (not reserved) | Satisfied — `real` is not `suite`, not `_`-prefixed. |

`real.yaml` is the worked example of the convention; no migration required. Recorded explicitly in `artifacts/D-0108/spec.md` §"Out of scope for T06.04".

## OQ-6 resolution evidence

`decisions.md` §"DOC-OQ6 Closure" §"Closure of OQ-6" (lines 731-736):

> - **Question:** Suite filename convention beyond `real.yaml` (e.g., quick subset).
> - **Resolution:** Filename convention ratified at
>   `src/superclaude/cli/eval/suites/README.md` (§"Filename rules").
>   `*.yaml` lower-case extension; `snake_case` stem matching
>   `[a-z][a-z0-9_]*`; stem MUST equal manifest `name:` field; stem
>   unique per directory; reserved stems `suite` and `_`-prefixed.
>   `quick.yaml` is recorded as a deferred follow-up in the same
>   README (§"Planned follow-up — `quick.yaml`") with shape,
>   scope-exclusions, and trigger conditions documented; no v1 work,
>   no schema changes, no loader changes required.
> - **Resolution status:** RESOLVED — 2026-05-20.
> - **Resolution artifact:** This section (`decisions.md` §"DOC-OQ6
>   Closure") + `src/superclaude/cli/eval/suites/README.md` +
>   `artifacts/D-0108/spec.md`.

## OPS-001 §B audit-trail evidence

OQ-6 is **not** a row in the OPS-001 §B table because the §B table was authored at T01.25 against M1-scoped OQs (OQ-1 / OQ-3 / OQ-7 / OQ-8 / OQ-10). OQ-6 was opened against M5 (roadmap row 332). The R8 update note (line 493) records OQ-6's RESOLVED status without editing the §B table charter:

> **Update (R8, 2026-05-20 — T06.04):** OQ-6 (not in the §B table
> above because it was opened against M5 not M1; roadmap row 332)
> has flipped OPEN → RESOLVED via DOC-OQ6 closure — suite filename
> convention recorded at `src/superclaude/cli/eval/suites/README.md`,
> `quick.yaml` recorded as a deferred follow-up (no v1 work). See
> §"DOC-OQ6 Closure" below for the full rationale. OQ-3 and OQ-10
> remain DEFERRED per design.

Rationale for the choice not to insert OQ-6 into the §B table itself is in `artifacts/D-0108/notes.md` §6.

## DOC-OQ6 acceptance crosscheck

Roadmap row 351 (DOC-OQ6 / R-107) AC: *"cli/eval/suites/README.md records naming convention; `quick.yaml` plan recorded as follow-up."*

| AC element | Satisfied at |
|------------|--------------|
| `cli/eval/suites/README.md` records naming convention | `src/superclaude/cli/eval/suites/README.md` §"Filename rules" (rules 1-5). |
| `quick.yaml` plan recorded as follow-up | `src/superclaude/cli/eval/suites/README.md` §"Planned follow-up — `quick.yaml`" (deferral rationale, intended shape, scope exclusions, trigger conditions). |

Both AC elements satisfied. The ADR-log entry at `decisions.md` §"DOC-OQ6 Closure" provides the cross-referenced revision-log surface; the README is the working source.

## Cross-link

- Evidence summary: `.dev/releases/current/cliEval/evidence/T06.04/summary.md`
- ADR log: `.dev/releases/current/cliEval/decisions.md` (R8, §"DOC-OQ6 Closure")
- Companion spec: `artifacts/D-0108/spec.md`
- Design rationale: `artifacts/D-0108/notes.md`
- Authoritative source (README): `src/superclaude/cli/eval/suites/README.md`
- Downstream consumers:
  - T06.09 (SC5 OQ-1..OQ-10 ledger; reads OQ-6 as RESOLVED with this closure as resolution evidence)
  - T06.16 (M6 exit checkpoint; inherits OQ-6 resolution)
  - Future follow-up RF task that lands `quick.yaml` (consumes the README §"Planned follow-up" contract; amends the README inventory; may add a one-line `Outcome:` to the DOC-OQ6 closure)
