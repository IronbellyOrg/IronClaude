# Phase 1 Prereq Check — CLI Flag Verification

**Date:** 2026-04-02

## roadmap run --help

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| `--prd-file` option present | Yes | Yes — "Path to a PRD file for supplementary business context enrichment" | PASS |
| `--tdd-file` option present | Yes | Yes — "Path to a TDD file for supplementary technical context enrichment" | PASS |
| Positional arg is `INPUT_FILES` | Yes | Yes — `INPUT_FILES...` with nargs=-1 | PASS |
| Help mentions "1-3 markdown files" | Yes | Yes — "INPUT_FILES accepts 1-3 markdown files (spec, TDD, PRD) in any order" | PASS |
| Multi-file usage examples | Yes | Yes — `spec.md`, `spec.md tdd.md`, `spec.md tdd.md prd.md` | PASS |
| `--input-type` choices `[auto\|tdd\|spec]` | No "prd" | `[auto\|tdd\|spec]` — no "prd" | PASS |
| `--input-type` mentions PRD auto-detection | Yes | Yes — "PRD files are auto-detected when passed as positional arguments" | PASS |

## tasklist validate --help

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| `--prd-file` option present | Yes | Yes — "Path to the PRD file used as an additional validation input" | PASS |
| `--tdd-file` option present | Yes | Yes — "Path to the TDD file used as an additional validation input" | PASS |

## --input-type prd rejection test

```
$ uv run superclaude roadmap run --input-type prd .dev/test-fixtures/test-spec-user-auth.md --dry-run
Error: Invalid value for '--input-type': 'prd' is not one of 'auto', 'tdd', 'spec'.
Exit code: 2
```
Result: PASS — "prd" correctly rejected as invalid CLI choice.

## Overall: ALL CHECKS PASS
