# sc-swarm-wizard-protocol — 5-round optimization + testing summary

Autonomous/headless skill-creator loop. Baseline value established in R1; later rounds run with-skill
(targeted feature/regression validation) since the discriminating baseline gap was already proven.

## Round 1 — behavioral baseline (3 scenarios × {with-skill, baseline})
With-skill **17/17 assertions PASS**. Baseline failed where it counts: mis-mapped goal→lens (chose
bare-review for an edge-case goal; wrong reviewer default), and launched a real run with no go-ahead.
**Fixes found:** (1) proxy-404 diagnostic (real `:4000/cli` base + appended `/chat/completions` → 404);
(2) reassure novices about the harmless `uv run` VIRTUAL_ENV warning.

## Round 2 — apply fixes + harder scenarios (3 with-skill)
All PASS. Ambiguous goal → correctly disambiguated by tie-breaker (not silently picked). doc-completeness
mapped correctly (3 workers, /sc:document). **Real run launched (env present) → all workers HTTP 404 →
the new proxy-404 matrix row fired with the correct plain-language diagnosis, no fabrication, honest
failure summary.** Directly validates the R1 fix.

## Round 3 — adversarial conformance audit + trigger eval
Trigger eval **12/12** (8 positives, 4 near-miss negatives) — description triggers cleanly, no change
needed. Audit found: **C1 CRITICAL** — skill `name:` was hyphenated (`sc-…`) but Activation/exemplar use
colon (`sc:…`); would break the command→skill handoff. **M1** contradictory `cancelled` status wording.
**M2** stray code fence in summary template. **L2** misleading `--resume`+`--lens` boundary. **All fixed.**
H1 (framework-file registration) **downgraded** — verified that shipped exemplars (pr-submit, reflect,
roadmap, brainstorm) are NOT registered in the stale COMMANDS.md/ORCHESTRATOR.md/FLAGS.md, so matching
repo reality = don't edit those. Factual accuracy vs ground truth: all spot-checks PASS.

## Round 4 — edge STOP gates (2 with-skill, against the fixed skill)
Both PASS (also serves as post-fix regression). Too-small target → **stopped before running**, plain
explanation, no raw rule code leaked, helpful next step. Advanced custom-lens → rejected bare
`--lens custom`, gave the arbitrary-code trust warning, advanced-gated, correct spec-file plan.

## Round 5 — deterministic validation gates
`make sync-dev` → `make verify-sync` → markdownlint on the new files → frontmatter sanity. See
ITER5-GATES.md.

## Net
With-skill behavioral pass rate across rounds: 100%. One CRITICAL structural defect (C1) caught by the
adversarial audit and fixed. Skill is grounded in an empirically-verified facts-sheet and re-grounds on
the live `--help` every run, so it survives CLI drift.
