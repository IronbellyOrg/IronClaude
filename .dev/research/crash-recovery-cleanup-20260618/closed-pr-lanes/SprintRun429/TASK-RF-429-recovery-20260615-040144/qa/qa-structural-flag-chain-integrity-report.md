# QA Report — Structural Flag-Chain Integrity (`--max-session-resets`)

**Verdict (binary): PASS**

**Topic:** 4-hop `--max-session-resets` operator-flag chain + P3 policy-read closure
**Date:** 2026-06-18
**Phase:** report-validation (single-lens structural trace)
**Fix cycle:** N/A
**Fix authorization:** false (report only — no files edited)
**Lens scope:** ONLY the `--max-session-resets` flag chain. No other findings reported.

---

## Adversarial result

I assumed at least one hop was broken and tried to find the break. I could not find one.
All four hops AND both closure sites resolve, and the dataclass field is confirmed to exist
at runtime (`dataclasses.fields(SprintConfig)` → `max_session_resets`, default `8`), so the
`getattr(config, "max_session_resets", 8)` calls in executor.py return the **real operator
field**, not the hardcoded `8` fallback. The chain is intact.

---

## Items Reviewed

| # | Hop / Check | Result | file:line evidence |
|---|-------------|--------|--------------------|
| 1 | Hop 1 — `@click.option("--max-session-resets", "max_session_resets", type=int, default=8, show_default=True, ...)` | PASS | `commands.py:233-241` (option decl); dest name `max_session_resets` at `:235` |
| 2 | Hop 2a — `run()` signature has `max_session_resets: int` | PASS | `commands.py:267` (param in `run(...)` signature `:243-268`, after `@click.pass_context` `:242`) |
| 3 | Hop 2b — `load_sprint_config(...)` call passes `max_session_resets=max_session_resets` | PASS | call opens `commands.py:347`; arg at `commands.py:364` (`max_session_resets=max_session_resets`) |
| 4 | Hop 3a — `load_sprint_config` DEF param `max_session_resets: int = 8` | PASS | `config.py:298` (in DEF signature `:282-299`) |
| 5 | Hop 3b — forwards `max_session_resets=...` into `SprintConfig(...)` | PASS | `SprintConfig(` construction opens `config.py:348`; arg at `config.py:370` (`max_session_resets=max_session_resets`) |
| 6 | Hop 4 — `SprintConfig` dataclass field `max_session_resets: int = 8` | PASS | `models.py:611` (real field; `:607-610` are comments). Enclosing class = `@dataclass class SprintConfig(PipelineConfig)` (`models.py:537-538`). Defined exactly once (grep count = 1). |
| 7 | Closure K>1 — `SessionResetPolicy(max_session_resets=getattr(config, "max_session_resets", 8))` | PASS | `executor.py:1334-1336`. `config: SprintConfig` (enclosing-fn type). Field exists → getattr returns real field. |
| 8 | Closure K=1 — same construction at sequential/single-session site | PASS | `executor.py:1901-1903` (`getattr(config, "max_session_resets", 8)`). |
| 9 | getattr-not-defaulting (the silent-default trap) | PASS | Runtime: `dataclasses.fields(SprintConfig)` contains `max_session_resets`, default `8`. Field present ⇒ getattr returns operator value, NOT the `8` literal fallback. |

## Summary

- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None. No dropped hop, no shadowed field, no base-class redefinition, no field-ordering
TypeError, no broken pass-through.

## Adversarial probes that came back clean

| Probe | Why it could break the chain | Result |
|-------|------------------------------|--------|
| Duplicate field def | A second `max_session_resets` could shadow with a different default | `grep -c "^    max_session_resets"` = **1** (models.py) |
| Base-class redefine | `PipelineConfig` could define it with a conflicting default | `grep -rn max_session_resets src/.../pipeline/` = **none** |
| Field-ordering TypeError | Non-default field after default field → dataclass def fails at import | Import succeeded; runtime field-read worked |
| getattr silently defaulting | If the field were missing, `getattr(..., 8)` returns `8` and the flag is dead | Runtime confirms field **present**, default `8` → real field returned |
| Click dest mismatch | `@click.option` dest must equal `run()` param name | Both literally `max_session_resets` (`commands.py:235`, `:267`) |
| Pass-through to wrong constructor | `:370` could land in a non-`SprintConfig` object | `:370` is inside `SprintConfig(` opened at `config.py:348` |

## Confidence

**Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

Every item is backed by either a Read of the cited lines, a grep, or a runtime
`dataclasses.fields` check — not by trusting the p5-aggregate manifest claims.

**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 6 (4 greps + 1 class-locate + 1 runtime field check)

## Notes on the closure design (informational, not a finding)

Both executor sites intentionally use `getattr(config, "max_session_resets", 8)` rather than
direct attribute access `config.max_session_resets`. The inline comment at `executor.py:1332`
("The getattr bridges until P5 adds SprintConfig.max_session_resets") shows this was a P3→P5
sequencing bridge. Now that P5 added the real field (hop 4), the getattr is harmless — it
resolves the genuine field. It is slightly weaker than direct access (a future field rename
would silently revert to `8` instead of raising `AttributeError`), but that is a robustness
nuance, not a chain break, and is out of this lens's scope.

## QA Complete
