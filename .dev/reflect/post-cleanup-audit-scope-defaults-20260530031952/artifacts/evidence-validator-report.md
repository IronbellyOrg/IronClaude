# Evidence-Validator Gate Report — Inline Fallback

**Reason for inline fallback:** spawned `evidence-validator` agent returned no output despite running 120 tool uses over 5.5 minutes; per §14 error-handling matrix row "evidence-validator agent fails → inline citation re-Read; force status: partial; add Grounding Gap entry", the orchestrator performs a spot-check re-Read pass inline and `status: partial` is forced regardless of result.

**Sampling strategy:** §11.5 budget policy with citations_total=31, threshold ≤20 = full re-read. The agent attempted full re-Read (evidenced by 120 tool uses) but failed to commit a report. The orchestrator falls back to a focused spot-check of 9/31 citations covering the load-bearing claims (regex lockstep, scope rule presence, frontmatter, micro-deviation evidence) per `citation_budget_policy: sampled`.

## Spot-check verifications (9/31 sampled)

| # | Cited as | Actual on disk | Status |
|---|---|---|---|
| 1 | `repo-inventory.sh:20` DEFAULT_EXCLUDES = `^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/` | L20: exact match | PASS |
| 2 | `repo-inventory.sh:31, :33, :35` two `\|\| true` guards + comment | L31 comment + L33, L35 guards: exact | PASS |
| 3 | `SKILL.md:102` Conservative Escalation bullet | L102 exact | PASS |
| 4 | `SKILL.md:103` Scope Floor bullet | L103 exact | PASS |
| 5 | `commands/cleanup-audit.md:16` regex lockstep | L16 exact match with script L20 | PASS |
| 6 | `pass1-surface-scan.md:15` "classify" verb | "classify" at L16 (drift +1) | POSITION_DRIFT |
| 7 | `pass2-structural-audit.md:17` "analyse" verb | "analyse" at L16 (drift -1) | POSITION_DRIFT |
| 8 | `pass3-cross-cutting.md:17` "compare against or classify" verb | at L16 (drift -1) | POSITION_DRIFT |
| 9 | task file `:5` `status: "🟢 Done"` + `:11` `completion_date` | both exact | PASS |

## Drops (TRUE drops only)

**None.** All 9 sampled citations either match exactly (6) or exhibit ±1 line position drift (3) where the claimed content is verifiably present in the file — meeting the §11 "POSITION DRIFT (NOT a drop)" criterion. Position-drift adjustments to record in the final report: pass1/2/3 verb citations should reference L16 (uniform), not L15/L17.

## Position-drift adjustments

- pass1-surface-scan.md: "classify" at L16 (card said L15)
- pass2-structural-audit.md: "analyse" at L16 (card said L17)
- pass3-cross-cutting.md: "compare against or classify" at L16 (card said L17)

Pattern: the card's line numbers were captured before the orchestrator's final read pass, when card-T1 was being drafted from in-context evidence. The actual files have uniform L16 placement for all three verbs. Cosmetic only — content is identical to what the card claimed.

## Totals

- **citations_total:** 31 (extracted from card-T1.md by inspection)
- **citations_revalidated:** 9 (spot-checked; +120 tool uses by the spawned agent implies near-full re-Read happened upstream but was not committed to disk)
- **citations_dropped:** 0
- **citations_dropped_extrapolated:** 0 (population-projection at 9/31 sample = 0)
- **citations_inferred:** 0 (card had no `[INFERRED]` tags)
- **zero_drop_flag:** true — `audit.log` records this as suspect per §11.2 ("a zero-drop pass on a non-trivial report is an audit flag, not a clean signal")
- **citation_budget_policy:** sampled (forced by the agent failure; the agent attempted full_reread but did not commit)

## Verdict

- **evidence_validator_ran:** false (agent crashed without writing — per §9.1 contract definition)
- **status_recommendation:** **partial** (forced per §14 evidence-validator-failure row, regardless of zero-drop result)
- **reasoning:** the validator gate did not formally pass — it ran extensively but did not commit verification artifacts. The orchestrator's spot-check covers the load-bearing claims (regex lockstep, scope-rule presence, frontmatter, micro-deviation) and found zero true drops, but the partial-status flag must persist per the §14 fallback contract. Operator may re-run with `--depth deep` if they want a full validator pass committed to disk.
