# Evidence — T02.01: Add usage section to sandbox index

- **Task:** T02.01 (Roadmap R-003, Deliverable D-0003)
- **Target file:** `.dev/e2e-reflect/tl-1/work/index.md`
- **Date:** 2026-06-06

## Change

Added a `## Usage` section to `index.md` containing a relative markdown link to `glossary.md`.

## Verification

| Acceptance Criterion | Result |
|---|---|
| `index.md` contains a `## Usage` section | PASS (`grep "^## Usage"` → line 5, count = 1) |
| `index.md` contains a markdown link to `glossary.md` | PASS (`[glossary](glossary.md)` at line 7) |
| Update is repeatable without duplicating the Usage section | PASS (single `## Usage` heading; `grep -c "^## Usage"` = 1) |
| Evidence recorded at this path | PASS (this file) |

## Command output

```
$ grep -n "^## Usage" .dev/e2e-reflect/tl-1/work/index.md
5:## Usage
$ grep -n "glossary.md" .dev/e2e-reflect/tl-1/work/index.md
7:For definitions of the terms used in this bundle, see the [glossary](glossary.md).
$ grep -c "^## Usage" .dev/e2e-reflect/tl-1/work/index.md
1
```

**Status: PASS**
