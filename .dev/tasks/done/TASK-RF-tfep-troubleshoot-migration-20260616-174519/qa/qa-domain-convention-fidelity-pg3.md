# QA Report — Domain Lens: Convention Fidelity (Phase 3 Gate)

**Topic:** Wiring `--context` / `--caller` into /sc:troubleshoot — convention-fidelity verification
**Date:** 2026-06-16
**Phase:** synthesis-gate (domain QA lens — convention fidelity)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Stance:** Adversarial — assumed ≥5 deviations; verified every claim against the in-file exemplars.

---

## Overall Verdict: FAIL

Two backtick-convention deviations found, both on `commands/troubleshoot.md` line 69. The new
`(if caller=task-unified)` conditional clause drops inline-code backticks on two tokens that the
file (and the rest of line 69) backticks everywhere else. The three primary conventions named in
the spawn brief — `(none)` default sentinel, lowercase-key `<placeholder|none>` audit-block style,
and the parenthetical-conditional surface style — all hold at the **structural** level, but the
parenthetical-conditional exemplars `(if `--fix`)` and `(if `pipeline_hardening_applicable`)` both
backtick their inner token, and the new sibling does not. Under zero-tolerance convention fidelity
this is a FAIL: the new conditional does not match the exact rendering of the two exemplars it was
modeled on.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `(none)` unbacktick default sentinel in new Options rows matches existing `--scope` row | PASS | command L52 `--scope` = `(none)`; L59 `--context` = `(none)`; L60 `--caller` = `(none)`. Byte-identical sentinel, unbackticked. (`--models` uses `(agent defaults)`, also unbacktick — consistent family.) |
| 2 | lowercase-key `<placeholder\|none>` for `caller:` / `context_path:` in TARGET header matches `scope: <path\|symbol\|none>` | PASS | SKILL L133 `scope: <path\|symbol\|none>`; L138 `caller: <name\|none>`; L139 `context_path: <abs-path\|none>`. All lowercase keys, all `<...\|none>` form. |
| 3 | lowercase-key `<placeholder\|none>` for `caller:` / `return_contract_path:` in SUMMARY footer matches same style | PASS | SKILL L460 `caller: <name\|none>`; L461 `return_contract_path: <abs-path\|none>`. Matches TARGET convention exactly. |
| 4 | parenthetical-conditional surface style `(if caller=task-unified)` matches `(if --fix)` / `(if pipeline_hardening_applicable)` | FAIL | command L69: exemplars render `(if `--fix`)` and `(if `pipeline_hardening_applicable`)` — inner token **backticked**. New clause renders `(if caller=task-unified)` — inner token **NOT backticked**. Deviation. See Issue #1. |
| 5 | (adversarial-adjacent) `return-contract.yaml` backtick consistency for the new clause | FAIL | `return-contract.yaml` is backticked at command L59, L60 and SKILL L143; on command L69 it renders bare ("the emitted return-contract.yaml path"). Same line, same deviation class. See Issue #2. |
| 6 | argument-hint placeholder style for `--context`/`--caller` matches `--scope` | PASS | command L8: `[--context <path>]`, `[--caller <name>]` mirror `[--scope <path\|symbol>]` and `[--output-dir <path>]`. |
| 7 | Flag-list completeness: SKILL Wave 0 step 1 and command argument-hint both register `--context` + `--caller` | PASS | SKILL L115 flag list includes `--context`, `--caller`; command L8 argument-hint includes both. No orphaned flag. |
| 8 | `task-unified` value backtick treatment in Options row | PASS (but see Issue #1 cross-ref) | command L60 renders `` `task-unified` `` backticked as a value mention; the bare `caller=task-unified` on L69/L143 is the inconsistency captured under Issue #1. |

## Summary

- Checks passed: 6 / 8
- Checks failed: 2
- Critical issues: 0
- Important issues: 2 (both surface-cosmetic backtick deviations, same line, same root)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `src/superclaude/commands/troubleshoot.md:69` | New parenthetical conditional `(if caller=task-unified)` does NOT backtick its inner token, while the two sibling exemplars on the same line do: `(if `--fix`)` and `(if `pipeline_hardening_applicable`)`. The spawn brief named exactly those two as the convention to match. Deviation in the parenthetical-conditional surface style. | Render as `` (if `caller=task-unified`) `` to match the backticked inner-token style of the sibling conditionals. (Alternatively, if the intended convention is to backtick only the identifier, `(if `caller`=task-unified)` — but the cleaner match to `(if `--fix`)` is to backtick the whole predicate.) |
| 2 | IMPORTANT | `src/superclaude/commands/troubleshoot.md:69` | `return-contract.yaml` is rendered **bare** in the new clause ("the emitted return-contract.yaml path"), but is backticked as a code-identifier everywhere else it appears: L59, L60, and SKILL L143 (`` `return-contract.yaml` ``). Inline-code backtick convention broken for the new clause only. | Render as `` `return-contract.yaml` `` on L69 to match its treatment on L59/L60/L143. |

## Convention-Fidelity Detail

**Convention 1 — `(none)` unbacktick sentinel.** Held. The new `--context` and `--caller`
rows both use the bare `(none)` token, byte-identical to the existing `--scope` row default. No
backticked-default deviation (the failure mode the brief flagged) is present. The boolean-flag rows
(`--no-mcp`, `--no-escalate`, `--fix`) use backticked `` `false` `` — a different and correct
family (booleans), so the unbacktick `(none)` for path/name-valued flags is internally consistent.

**Convention 2 — lowercase-key `<placeholder|none>` audit blocks.** Held in both blocks. New keys
`caller:`, `context_path:` (TARGET) and `caller:`, `return_contract_path:` (SUMMARY) are all
lowercase, snake_case, and use the `<…|none>` / `<abs-path|none>` placeholder form matching the
existing `scope: <path|symbol|none>` and `output_dir: <abs-path>` style. No uppercase-key deviation,
no alternate placeholder syntax (`{…}`, `[…]`, `VALUE`) anywhere in the new keys.

**Convention 3 — parenthetical-conditional surface style.** FAILED on backtick fidelity. The
structural shape `(if <predicate>) <consequence>` matches the exemplars, but the exemplars backtick
the predicate token and the new clause does not. This is the load-bearing deviation: the brief
explicitly anchored the convention to `(if `--fix`)` and `(if `pipeline_hardening_applicable`)`,
both of which backtick. Note this is a command-file finding; the SKILL-side prose use of bare
`caller=task-unified` (L143) and `When caller=task-unified` is NOT a parenthetical-conditional (it
is running prose introduced by "When"), so it is not in scope for Convention 3 — but it shares the
same bare-token treatment and is worth aligning if the fix touches backtick consistency broadly.

## Confidence Gate

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 6 (each Bash a targeted grep/sed against a specific convention claim)

Every check maps to a specific tool-verified line citation. No item relied on another report.
No web research required (all claims are intrinsically local to the two files). Tavily not engaged;
no fallback.

## Recommendations

- Resolve BOTH backtick deviations on `commands/troubleshoot.md:69` before this gate passes.
  They are cosmetic but the gate is convention-fidelity with zero tolerance — surface style IS the
  deliverable here.
- Recommended single-line replacement target for L69: change
  `…and (if caller=task-unified) the emitted return-contract.yaml path.`
  →
  ``…and (if `caller=task-unified`) the emitted `return-contract.yaml` path.``
- After fix, re-run convention-3 + return-contract backtick checks only (the other 6 checks PASS and
  need no re-verification).
- Optional alignment (out of strict scope): SKILL L143 prose `caller=task-unified` is bare; the
  Options row L60 backticks `` `task-unified` ``. Not a Convention-3 violation (it is prose, not a
  parenthetical conditional), but flagged for whoever owns broad backtick consistency.

## QA Complete
