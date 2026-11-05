# Merge Log

## Metadata
- Base: Variant 1 (`variant-1-original.md`, reviewer-1 card, calibrated C=0.75)
- Incorporated: Variant 2 (`variant-2-original.md`, reviewer-2 card, calibrated C=0.77), findings R2-F1 and R2-F2
- Plan: `refactor-plan.md` (14 changes, auto-approved 2026-10-29)
- Executor: merge-executor (sc:adversarial Mode A, Step 5)
- Output: `../merged-findings.md`
- Changes applied: 14 of 14 (0 skipped, 0 escalated)
- Status: SUCCESS, YAML validated
- Timestamp: 2026-10-29

## Changes Applied

| # | Target | Status | Before | After |
|---|---|---|---|---|
| 1 | R1-F1 | applied | IMPORTANT; "fails on many more files; T1's fix too narrow"; 8 evidence refs incl. SKILL.md:5/147/550, reflect.md:169/171 | MINOR, spec-inherited; exactly two lines remain (contract.py:30, rubric:127); evidence trimmed to plan:167, plan:172, source.md:421 and the two lines; fix = Task 7 comment drop (28-34) + Task 12 pull-forward or exclude |
| 2 | R1-F2 | applied | IMPORTANT; fix offers "list non-T9 files or scope rg" | MINOR, spec-inherited; claim adds 49 `mcp-servers:` lines and the T10/T11 rows; evidence adds source.md:392; fix = Task 10 drops `serena` from every line (G5) |
| 3 | R1-F3 | applied | IMPORTANT; fix includes "add to Task 5's rg" | IMPORTANT, spec-inherited; claim adds test mechanics (install_mcp.py:766-769, tavily :426-430, :926-929, :943-945, source.md:334/335); rg sub-fix removed |
| 4 | R1-F4 | applied | IMPORTANT; "sandbox rg has no allowlist" | IMPORTANT, spec-inherited; rewritten as (a) vacuous pass on hidden paths and (b) allowlisted text plus `settings.json.bak.*`; fix = `--hidden --no-ignore` + line-level `rg -v` filter + bak assertion |
| 5 | R1-F5 | applied | IMPORTANT; fix covers update.sh and Tier K only | IMPORTANT, spec-inherited; claim adds latent status and plan:80; fix covers every `env` call incl. `--force`/doctor and no-CLI run |
| 6 | R1-F6 | applied | IMPORTANT; fix = widen to 124-130 | MINOR, spec-inherited; claim adds INV-005 ref lines; fix = per-line rubric actions, INV-005 lines, G8 note, keep "No-mutation gate." |
| 7 | R1-F7 | applied | MINOR | MINOR, plan-introduced, text unchanged |
| 8 | R1-F8 | applied | MINOR, 3 evidence refs | MINOR, plan-introduced; evidence adds the two absent directories (INV-009) |
| 9 | R1-F9 | applied | MINOR | MINOR, plan-introduced, text unchanged |
| 10 | R1-F10 | applied | MINOR, grounded: false, ledger + main.py halves | MINOR, plan-introduced, grounded: true; ledger half only; evidence = plan:21 + session git status; fix = Tasks 13/14/15/19 `git add` exact paths |
| 11 | R2-F1 | applied | (V2) MINOR, "carried by no plan task and no Constraint" | MINOR, plan-introduced, coverage-gap; narrowed (plan:26 already blocks real-HOME etc.); fix = INV-007 Constraints bullet |
| 12 | R2-F2 | applied | (V2) MINOR, "rg check can therefore pass" | MINOR, spec-inherited; "can therefore pass" removed; evidence adds install_core.py:65-70, install_commands.py:55-61; fix expects the change-4 filtered rg to print nothing |
| 13 | header `spec_errata` | applied | absent | 6 entries: T9 rg, T10b rg, §3.5, DoD-2/T14 4-5, P84, DoD-3 vs T14 step 5 |
| 14 | header `dropped_subclaims`, `process_notes` | applied | absent | 5 dropped rows (C-001, C-003, C-010, C-004, S-002); 1 process note (`mkdir -p /tmp/x`) |

Mechanical notes (no strategic choice): plan shorthand `plan:N` and `source.md:N` was expanded to full repo paths in `evidence` lists and kept as shorthand inside `claim`/`fix` text. Installer and reflect-ref paths named without directories in the plan were resolved by Glob before writing (`src/superclaude/cli/install_{skill,hooks,user_setup,core,commands}.py`, `src/superclaude/skills/sc-reflect-protocol/refs/*`); all exist. Evidence that only supported a dropped sub-claim (R1-F1 SKILL.md/reflect.md refs; R1-F10 main.py:292/313 and plan:91) was removed with that sub-claim.

## Post-Merge Validation

- YAML parse: `yaml.safe_load` on the single fenced block (extracted inline, no helper files) succeeded.
- Findings: 12; ids unique; order R1-F3, R1-F4, R1-F5, R1-F1, R1-F2, R1-F6, R1-F7, R1-F8, R1-F9, R1-F10, R2-F1, R2-F2 (matches requested order).
- Severity: IMPORTANT 3, MINOR 9; header `counts {kept: 12, dropped: 0, important: 3, minor: 9}` matches the computed values.
- Schema: every finding has id, decision, merged_severity, deviation_class, class, claim, evidence (non-empty list), grounded (all true), fix, provenance. No missing fields.
- Header: merged_from (2 entries), method, convergence 0.947, verdict refactor present; spec_errata 6, dropped_subclaims 5, process_notes 1.
- Regex escaping: R1-F4 fix parses to `'/\.claude/skills/ccsession-tag/install\.sh:'` (single backslash, as intended).
- Provenance: each finding has a `# Source:` comment naming its variant and plan change number, plus a `provenance` field.
- Contradiction re-scan: none found.
  - R1-F3 fix no longer adds a Task 5 rg; consistent with dropped C-003.
  - R1-F10 no longer claims the main.py gap; consistent with dropped C-010.
  - R1-F4 excludes `claude-calls.log` only for `$T/fresh`; consistent with dropped C-004.
  - R2-F2 depends on the R1-F4 filter and no longer says the unfiltered rg passes; consistent with R1-F4 (b).
  - R1-F10 (stage handoff files) vs R2-F1 (only new `.dev` writes are in `.dev/codegraph-migration/handoffs/`): the ledger is `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` (plan :185), so the two agree.
  - R1-F1 cites the contract.py comment as 28-34 (plan) rather than 28-31 (base); plan wording used throughout, no remaining 28-31 reference.

## Summary
All 14 planned changes were applied to the Variant 1 base without escalation. The merged card holds 12 kept findings (3 IMPORTANT: R1-F3, R1-F4, R1-F5; 9 MINOR), 7 spec-inherited and 5 plan-introduced, with spec errata, 5 dropped sub-claims and 1 process note. The YAML parses and passes the schema, count and contradiction checks.
