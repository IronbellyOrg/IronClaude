---
status: merge-complete
base: variant-2-sonnet-refactorer
date: 2026-09-24
convergence: 0.80
---

# Merge log — sc-implement-rewrite

Executor applied binding decisions. No debate reopened.

## Inputs

| Role | Path |
|---|---|
| Base | `adversarial/variant-2-sonnet-refactorer.md` |
| Steal | `adversarial/variant-1-opus-architect.md` |
| Steal | `adversarial/variant-3-haiku-qa.md` |
| Seed | `seed-brief.md` |

## Outputs

- `/config/workspace/IronClaude/.dev/brainstorms/20260924-192715-sc-implement-rewrite/adversarial/merged-output.md`
- `/config/workspace/IronClaude/.dev/brainstorms/20260924-192715-sc-implement-rewrite/merged-requirements.md` (identical copy)

## Applied changes (plan order)

| # | Decision | Action | Source | Validation |
|---|---|---|---|---|
| 1 | Hard cutover; no pitch; no `--type/--framework/--safe/--with-tests` | Kept V2 R-015/R-020. Added V3 `E-LEGACY` even when a path is also present. | V2 + V3 | STOP table lists `E-LEGACY`. Banned flags not in Options. |
| 2 | Thin command + SKILL.md + `refs/qa.md` + `refs/ledger.md`. No Python CLI. No intake ref. | Overrode V2 N-002 (one optional spec-compliance.md) and V1/V3 third intake ref. Architecture is four files. | binding + V2 dispatcher | N-002 names exactly two refs. Out of scope lists Python CLI and `refs/intake.md`. |
| 3 | One existing spec/PRD/tasklist path. Enumerable markdown. Verb+object title = AC. Else `E-NO-AC`. Pitch-only = `E-NO-TASKS`. | Replaced V2 “single word still AC” and V1 wait-one-turn. QUALIFY is R-021. | V2 enumerate + V3 E-NO-AC + binding QUALIFY | R-002 / R-021 ACs falsifiable. |
| 4 | MDTM-shaped files execute this protocol. No `/task` invoke. `/task` only in Will-Not. | Overrode V1 R-016 STOP-and-point-at-`/task` and V3 `E-WRONG-TOOL`. | binding vs V1/V3 | R-017. Slim codes omit `E-WRONG-TOOL`. |
| 5 | Loop: implement → spec-compliance QA → extras. Verdict enum. Reviewer does not trust implementer. Evidence path:line or Ti.ACk; zero citations → cannot-verify. | Kept V2 extras-after. Added V3 citation obligation. Dropped V1 extras-before-QA and `spec-compliant` string. | V2 + V3 | R-004/R-005/R-008. Q0–Q8 order. |
| 6 | Reviewer: inline iff N≤3 AND source ≤400 lines AND not compacted; else one Task subagent. No `--reviewer`. | Tightened V2 “N=1 or N≤3…” to all three predicates. Dropped V1 `--reviewer` flag. | V2 + V1 isolation + binding | R-023. Flags table has no `--reviewer`. |
| 7 | Non-compliant → one fix pass → re-QA → HALT. `complete` on non-compliant only with operator Ruling. Executor must not author it. No `--force`. | Replaced V2 “fix or Ruling; do not advance” with V1 one-fix-then-HALT. Added V3 halt table + `E-HALT-QA` / `E-NO-RULING`. | V1 + V3 + binding | Halt table in §6. Ruling regex in §7. |
| 8 | Extras: pass/fail/skip/unrelated-red. Never spec verdict. Red suite disjoint = unrelated-red. | Kept V2 extras table. Vocabulary `unrelated-red` (not V2 `red-unrelated`, not V3 `ok`). | V2 + binding | R-008/R-009. Ledger extras regex. |
| 9 | Ledger `.dev/implement/<slug>/progress.md`. Header + parseable lines. Start-SHA before first edit. Resume = first latest-status not `complete`. Truncated last line → STOP. | Kept V2 path. Added V1/V3 start-SHA. Added V3 regex family and `E-LEDGER-CORRUPT`. | V2 + V1 + V3 | §7 exact grammar. R-010/R-011/R-022. |
| 10 | Whole-list: skip if N=1; else one pass default ON; optional skip. Not 6-agent, not reflect. | Kept V2 skip-on-N=1. Added `--skip-final-review` as the skip switch (no `--no-whole-list-review` name). | V2 + V3 flag name | R-012. |
| 11 | Parallel only if source marks independent; max 3. | Copied V2 R-003. | V2 | R-003. |
| 12 | No 20-task hard cap. Warn once at N≥20. | Dropped V3 `E-TOO-MANY` / Q6 cap. Added V1 warn-once text. | V1 + binding vs V3 | R-025. Slim codes omit `E-TOO-MANY`. |
| 13 | Copy V2 delete-table verbatim. | Copied V2 §4 table + “128 lines / rewrite; do not patch” + keep filename/slash/category. | V2 | §4 delete table. |
| 14 | Slim E-* only. | Nine codes. Folded V3 `E-EMPTY`/`E-SOURCE-UNREADABLE` into `E-NO-TASKS`/`E-SOURCE-MISSING`. Dropped `E-WRONG-TOOL`. | V3 slim list + binding | §5 STOP table. R-024. |
| 15 | Activation `Skill sc:implement-protocol`. lint-architecture / sync-dev. `.claude/` not SoT. | Kept V2 R-013/R-014/R-019. Copied V1 Activation block. | V2 + V1 | R-013/R-014/R-019. |
| 16 | Provenance HTML comments per major section. | `<!-- provenance: ... -->` on header and §§1–11. | binding | Present on every major `##`. |

## Dropped on purpose (not in merged spec)

- V1: `--reviewer`, `--fresh`, `--no-extras`, `--output`, three intake/qa/ledger refs as a trio, `spec-compliant` verdict, MDTM → STOP point at `/task`, extras-before-QA, YAML ledger frontmatter, TodoWrite in allowed-tools, eval-workspace fixtures as rewrite blockers.
- V3: `E-TOO-MANY` hard cap, `E-EMPTY`, `E-SOURCE-UNREADABLE`, `E-WRONG-TOOL`, `refs/intake.md`, `selfcheck.py` package, `--force` as a supported flag, `ok` extras vocabulary, 1-task FINAL still running.
- V2: “single word is still AC”; extras token `red-unrelated`; optional single `refs/spec-compliance.md`; “fix or Ruling” without a one-fix cap.

## Issues escalated

None. Every planned item applied. No improvisation beyond naming `--skip-final-review` as the concrete skip switch for decision 10 (V3 name; V1 had `--no-whole-list-review`).

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-24T19:48:07.881Z","contentHash":"82a41ab5","sections":[{"heading":null,"hash":"235c0f96"},{"heading":"Merge log — sc-implement-rewrite","hash":"69a3b4b3"},{"heading":"Inputs","hash":"4e6282ce"},{"heading":"Outputs","hash":"7aaedc20"},{"heading":"Applied changes (plan order)","hash":"52bd174a"},{"heading":"Dropped on purpose (not in merged spec)","hash":"b79a5d79"},{"heading":"Issues escalated","hash":"a2f6674b"}]}-->
<!--mc:threads:end-->
