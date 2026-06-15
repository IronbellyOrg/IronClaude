# Pipeline Hardening Closure

The **Pipeline Hardening Closure** mode is a protocol stage that runs after Tier-1 diagnosis and before report closure. It closes the **E1–E5 pipeline-escape class** — defects that live at a runtime, generated-artifact, shared-contract, or independent-review boundary, where a review can sign off from an *adjacent* proof (a command string, an edited helper, a PASS artifact, a generic evaluator path) while the real boundary still fails.

The mode runs an ordered wave pipeline **H0 → H5**. Each wave is an atomic, testable gate that rejects one specific *proof substitution*. Remediation is not "complete" until the protocol proves the invariant at the same boundary where the escape can recur — via reusable, mechanism-based gates rather than issue-specific patches.

This ref is the mode skeleton: trigger, the H0 applicability gate and boundary-scan schema, the H0 mechanism statement, and the H5 off-path-reviewer rule. The verdict-aggregation truth table, the output-contract field schema, and the waiver / no-re-greening latch live in [`hardening-output-contract.md`](hardening-output-contract.md). The per-wave gate mechanics live in [`runtime-entrypoint-verification.md`](runtime-entrypoint-verification.md) (H1), [`contract-enumeration.md`](contract-enumeration.md) (H2), [`unmask-and-sweep.md`](unmask-and-sweep.md) (H3), and [`effective-input-proof.md`](effective-input-proof.md) (H4).

## Trigger

The mode **auto-triggers by issue topology**, not by a CLI flag. After Tier-1 diagnosis, when the diagnosed issue touches a pipeline boundary (see the H0 trigger list below), H0 sets `pipeline_hardening_applicable = true` and the H1–H5 waves run before report closure. The invocation `/sc:troubleshoot <issue>` is unchanged; there is no `--hardening` flag (per the thin-command rule, NFR-5). When the issue does not touch a pipeline boundary, H0 sets `pipeline_hardening_applicable = false` and records the boundary scan that justifies the skip.

`pipeline_hardening_verdict` is the four-token enum `pass | blocked | advisory | not_applicable`. `advisory` is a first-class outcome (rationalized-N/A or accepted-substitute proof) and is never omitted.

## H0 — Applicability gate (FR-1)

H0 classifies whether the diagnosed issue is a pipeline escape / boundary change and sets `pipeline_hardening_applicable`.

- **When the issue touches any trigger boundary** — CLI/subprocess, file/stdin/prompt delivery, generated-artifact parser, gate/severity/status enum, duplicated evaluator, persisted/resume state, review/audit selector, sibling pipeline, or prior-escape unmask — set `pipeline_hardening_applicable = true`. H1–H5 then **cannot be silently skipped**: each wave MUST produce `PASS`, `FAIL`, or `N/A` with a valid rationale/waiver that feeds the §5.4 aggregation in [`hardening-output-contract.md`](hardening-output-contract.md).
- **When the mode is skipped**, the report records `pipeline_hardening_applicable = false`, a one-sentence reason, **and** the boundary scan that justifies the skip. A bare "looks local" reason is **invalid** — the skip must be backed by typed boundary-scan rows.

## H0 — Boundary scan row schema

Before `pipeline_hardening_applicable = false` can skip H1–H5, H0 emits one or more typed boundary-scan rows. Each row has these fields (per spec §5.6):

| Field | Required | Meaning |
|-------|----------|---------|
| `boundary_type` | yes | One of: `CLI/subprocess`, `file-stdin-prompt`, `generated-artifact-parser`, `gate-status-enum`, `duplicate-evaluator`, `persisted-state`, `review-selector`, `sibling-pipeline`, `prior-escape-unmask` |
| `producer` / `transformers` / `consumer` | yes | The concrete components in the data path |
| `evidence_source` | yes | File, command, report, or trace supporting the classification |
| `risk` | yes | Why this boundary can admit proof substitution |
| `decision` | yes | `applicable` or `not_applicable` |
| `rationale` | yes | One sentence; a bare `looks local` is invalid |

## H0 — Mechanism statement (FR-2)

H0 emits a one-paragraph, **feature-agnostic** mechanism statement (what class of boundary the escape lives at and what proof substitution it admits), plus a candidate `known_escapes_caught` set.

- The mechanism statement avoids feature-specific wording except where a feature is required as evidence.
- Each candidate escape ID in `known_escapes_caught` MUST be justified by the wave/card that would catch it. An escape ID may appear only if a passing wave/card is cited that would catch it (the FR-12 anti-inflation rule in [`hardening-output-contract.md`](hardening-output-contract.md)). An un-earned list that inflates coverage to E1–E5 is a defect.

## Verdict aggregation and the waiver / no-re-greening latch

After H0–H5 run, `pipeline_hardening_verdict` is a deterministic aggregation of the H-statuses plus `waiver_status`. The full 7-row truth table, the H5 decision-to-status mapping, the backtest-status-vs-verdict table, the output-contract field schema, and the one-way `waiver_status` latch (a waived or absent mandatory runtime probe downgrades the verdict to `blocked`/`advisory` and can **never** be re-greened to `pass`/`success` by a downstream stage) are all specified in [`hardening-output-contract.md`](hardening-output-contract.md). This ref defers to that contract for all verdict mechanics.

## H5 — Off-path reviewer rule + waiver standard (FR-11)

H5 decides whether off-path (independent) review is required and constrains waivers. `off_path_review_decision` is one of `required | performed | waived_with_rationale | not_required`.

- **Off-path review is `required`** when a CLI invokes a subprocess, paths are reinterpreted by another layer, generated artifacts feed later gates, persisted state affects resume, a review selector chooses a surface, a hard gate uses heuristic parsing, a mock substitutes for runtime I/O, a sibling has a divergent contract, or the change controls HALT/WARN/CONTINUE / data-loss / review-integrity.
- **A waiver is invalid** if it merely says the tests pass, the reviewer is independent, the command exists, or the issue looks local. A valid `waived_with_rationale` sets the one-way `waiver_status` latch and forces the verdict into `{blocked, advisory}` (see [`hardening-output-contract.md`](hardening-output-contract.md)); an invalid waiver maps to `FAIL`.

## Wave sequence

| Wave | Gate | Ref |
|------|------|-----|
| H0 | Applicability + mechanism + boundary scan | this ref |
| H1 | Runtime-entrypoint verification + negative witness | [`runtime-entrypoint-verification.md`](runtime-entrypoint-verification.md) |
| H2 | Contract-enumeration ledger + sibling sweep | [`contract-enumeration.md`](contract-enumeration.md) |
| H3 | Unmask-and-sweep classifier + allow-list grammar | [`unmask-and-sweep.md`](unmask-and-sweep.md) |
| H4 | Effective-input proof (fail-closed) | [`effective-input-proof.md`](effective-input-proof.md) |
| H5 | Off-path reviewer rule + waiver standard | this ref |
| verdict | Deterministic aggregation + waiver latch | [`hardening-output-contract.md`](hardening-output-contract.md) |
