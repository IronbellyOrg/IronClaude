# Severity Routing (C3) — re-grade by reference, then route to troubleshoot

This ref has **two crisply-separated halves**: **grade** (reused wholesale from the auggie-review
rubric — never copied) and **route** (the NEW C3-owned tier→troubleshoot map). Keeping the boundary
sharp is the whole point: the rubric is the single source of severity truth; drift between a copied
rubric and the source is exactly the failure this reuse-by-reference discipline prevents.

> **Core purity (NFR-6 / AC-9, T-N50).** This file and its module `severity_router.py` contain ZERO
> shell or version-control command tokens. Grading and routing are pure functions of the finding's
> fields; the dispatch I/O lives in `troubleshoot-dispatch.md` and the SKILL.

## 1. Grade — DEFER TO the rubric (reuse, do NOT copy)

Re-grading is **not** reinvented here. For every Augment finding, **apply the severity-remap
algorithm defined in `sc-auggie-review-protocol/refs/severity-rubric.md` §Severity-remap algorithm**
(the 5-step pipeline at `severity-rubric.md:63-101`), keyed on the rubric's **category floor/ceiling
table** (`severity-rubric.md:70-87`). The five steps, applied by reference:

1. Start from Augment's `severity_hint` (a hint, not authoritative — FR-3.1).
2. **Category floor/ceiling override** (`severity-rubric.md:70-87`) — the category is more reliable
   than the hint; clamp to the category's floor (minimum severity) and ceiling (maximum severity).
   E.g. `security (exploitable)` floor = Critical; `naming`/`style` ceiling = Nit.
3. **Confidence adjustment** (`:89-93`) — `low` → drop one tier; `medium`/`high` → no change.
4. **Diff-locality adjustment** (`:93-96`) — `in_diff:false` AND pre-existing-untouched → drop one tier.
5. **Cross-source agreement bonus** (`:97-100`, `--depth deep` only) — single-source → drop one tier
   unless the category floor blocks it.

The remapped tier is one of: Critical / High / Medium / Low / Nit. The module
`superclaude.pr_submit.severity_router.remap_severity(finding)` implements this pipeline by reference
(it encodes the category table the rubric defines; it does NOT fork the tier scheme). Tests assert
against the rubric's own calibration shapes (`severity-rubric.md:104-152`) so the reuse is provably
faithful (T-301 = the security-floor row; T-302 = the confidence-drop rule).

## 2. Route — NEW C3-owned tier→troubleshoot map (NOT in the rubric)

The rubric stops at producing a tier. The route map below is C3's own logic (FR-3.2). `route(finding)`
maps the **remapped** severity to a troubleshoot invocation form:

| Remapped tier | Troubleshoot route | Notes |
|---------------|--------------------|-------|
| Critical | `--depth deep --fix` | forces troubleshoot's Tier-2 escalation |
| High | `--depth deep --fix` | forces troubleshoot's Tier-2 escalation |
| Medium | `--fix` | `--fix` alone defaults to `--depth standard` (the safe form) |
| Low | report-only | NOT dispatched to troubleshoot |
| Nit | report-only | NOT dispatched to troubleshoot |

> **STOP — never emit `--depth quick --fix`.** `--depth quick` with `--fix` is an explicit
> troubleshoot conflict (`sc-troubleshoot-protocol/SKILL.md:131`). The Medium route is `--fix`
> (which defaults to `--depth standard`) — never "optimize" it to `--depth quick`. The route
> function asserts this invariant: it emits only `--fix`, `--depth deep --fix`, or `report-only`.

`--depth deep` is the lever that triggers troubleshoot's own Tier-2 escalation
(`escalation-rubric.md:60-61`); C3 does NOT reimplement that rubric — it only chooses the `--depth`
ordinal. The actual invocation string (issue seed + `--scope <file:line>` + `--type <category>`) is
constructed in `troubleshoot-dispatch.md` (C3b), for VERIFIED findings only.
