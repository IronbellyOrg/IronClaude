# Input parse + STOP

## Source

Exactly one: existing file (`@path` unwraps) **or** non-empty leftover prompt.

Inline prompt: persist `<run>/source.md` **before** `plan.md`.

Slug: `{prefix}-{hash8}` — prefix = first 24 `[a-z0-9_-]` of basename or prompt; hash8 = sha256[:8] of absolute path or full prompt.

Default output: `.dev/workflow/<slug>/`. `--output` MUST be under `.dev/workflow/`.

Overwrite same slug in place (no resume).

## STOP

| Code | When |
|------|------|
| `E-NO-SOURCE` | no path and no prompt, or two file tokens. No slug, no run dir, no yaml |
| `E-EMPTY-SOURCE` | whitespace-only |
| `E-BAD-FLAG` | unknown enum |
| `E-OUTPUT-PATH` | `--output` not under `.dev/workflow/` |
| `E-MISSING-DIR` | `--output` parent missing |
| `E-LEGACY` | `--parallel`, `--validate`, `--depth shallow\|normal` |
| `E-NO-PHASES` | Wave 1 extracted nothing |
| `E-GATE` | Wave 3 schema/heading fail |

Enums: strategy `systematic|agile|enterprise`; depth `quick|standard|deep`; handoff `none|design|implement|tasklist`.

Bash: mkdir of output dir only.
