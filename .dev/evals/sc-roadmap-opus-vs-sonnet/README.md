# sc:roadmap — Opus vs Sonnet adversarial-debate eval

## Purpose

Compare Opus and Sonnet roadmap variants under two input regimes, capturing the
Wave 2 adversarial debate transcript that critiques each variant's strengths
and weaknesses. Sample size: 5 paired runs per group, 10 total.

## Groups

| Group | Input regime | Source file | Lines |
|-------|--------------|-------------|-------|
| A | Spec only | `tests/sc-roadmap/fixtures/sample_spec.md` | 67 |
| B | PRD + TDD (concatenated) | `.dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md` | 1252 |

Both fixtures describe the same domain (User Authentication Service), so
within-group Opus-vs-Sonnet comparison is the primary signal; cross-group
comparison ("does richer input regime help?") is secondary and confounded by
the wide line-count gap.

## Pipeline paths

**Decision (post-pilot, 2026-05-22):** Primary eval uses **Path D (direct-mode)**
because Path R proved unreliable for the debate transcript (Group B pilot run
dropped it despite running 2 internal debate rounds). The 2 Path R pilot cells
are kept as reference but excluded from the primary 5+5 analysis set.

Pilot eval ran **two paths in parallel** to compare their artifact shape:

**Path R (roadmap-mode, primary):**
`/sc:roadmap <input> --multi-roadmap --agents opus,sonnet --depth standard --no-validate`

Runs Wave 1B (extraction) + Wave 2 (variant gen + debate via sc:adversarial) +
Wave 3 (merged roadmap.md / test-strategy.md). `--no-validate` skips Wave 4
multi-agent validation.

> **Lesson learned from earlier failed pilot:** `--dry-run` does NOT stop after
> the debate as the protocol text superficially implies. The executor treats it
> as a hard skip on sub-skill invocations that would write files — so under
> `--dry-run` the sc:adversarial step is *previewed but not executed*, and no
> variants or debate transcripts are produced. `--no-validate` is the correct
> flag for "run the debate, skip the final validator."

**Path D (direct-mode, side experiment):**
`/sc:adversarial --source <input> --generate roadmap --agents opus,sonnet --depth standard`

Bypasses sc:roadmap entirely. Runs the full 5-step adversarial protocol:
variant gen → diff → debate → base selection → merge → refactor plan. Different
artifact mix (no Wave 1B extraction.md / Wave 3 test-strategy.md, but adds
diff-analysis.md and refactoring-plan.md).

## Expected per-run artifacts

**Path R** (`group{A,B}/run{1..5}/`):

- `extraction.md` — Wave 1B extraction (FRs, NFRs, complexity, persona)
- `variant_opus_*.md` / `variant_sonnet_*.md` — variant roadmaps from each model
- `debate-transcript.md` — adversarial debate (2 rounds at `--depth standard`)
- `roadmap.md` — final merged roadmap (Wave 3 output)
- `test-strategy.md` — continuous validation strategy (Wave 3 output)
- `return-contract.yaml` — adversarial contract (convergence_score, base_variant, etc.)
- `session-stdout.log` / `session-stderr.log`

**Path D** (`group{A,B}-direct/run{1..5}/`):

- `variant_opus_*.md` / `variant_sonnet_*.md` — generated variants
- `diff-analysis.md` — structural + content diff between variants
- `debate-*.md` — adversarial debate output
- `base-selection.md` — hybrid scoring + base variant decision
- `refactoring-plan.md` — instructions to merge variants
- merged output file
- `return-contract.yaml`
- `session-stdout.log` / `session-stderr.log`

Exact filenames depend on the respective protocol's output schema.

## How to run

```bash
cd /config/workspace/IronClaude/.dev/eval-roadmap

# Pilot: 2x2 — 1 roadmap-mode + 1 direct-mode per group (4 cells, 2-at-a-time)
./run-eval.sh pilot

# Primary eval (direct-mode runs 2..5 for both groups, 4 batches of 2)
./run-eval.sh direct-remaining

# Full 5+5 direct-mode eval from scratch (10 cells)
./run-eval.sh direct-all

# Alternative: full 5+5 roadmap-mode eval (cheaper but unreliable on debate)
./run-eval.sh roadmap-all

# Single cell (useful for re-running a failed one)
./run-eval.sh single direct  A 3
./run-eval.sh single roadmap B 1

# After runs complete, aggregate metrics:
python3 ./aggregate.py .
```

Each `claude -p` subprocess runs with `--dangerously-skip-permissions`. The
script writes a `eval.log` at the eval root with start/end timestamps and per-
run return codes.

## Analysis (post-runs)

After 10 direct-mode runs complete, `aggregate.py` produces:

- `summary.csv` — machine-readable per-run metrics
- `summary.md` — per-run table + per-group aggregate stats

Manual analysis on top of that:

- **`debate-transcript.md`** + per-round files across runs: extract themes — categories where Opus consistently dominates, categories where Sonnet consistently dominates, points where the debate finds parity
- **Variant body comparison**: pick 1-2 runs per group, diff Opus-vs-Sonnet variant bodies on structure (milestone count, deliverable framing, risk register depth)
- **Persona drift impact**: which persona pairings showed up across the 10 runs, and whether convergence/winner correlates with persona choice (the persona confound)

Final report → `.dev/eval-roadmap/REPORT.md`.

## Known protocol quirks observed in pilot

- `return-contract.yaml` lands in different places across runs: sometimes
  `<run>/return-contract.yaml`, sometimes `<run>/adversarial/return-contract.yaml`.
  `aggregate.py` tries both.
- Per-round per-variant advocate/rebuttal files
  (`round1-variant1-advocate.md`, etc.) appear in some direct-mode runs but
  not others. When present, they're a richer audit trail than the single
  combined `debate-transcript.md`.
- Persona auto-inference for `--agents opus,sonnet` (no explicit persona) is
  non-deterministic: observed pairings include `default/default`,
  `security/security`, `architect/architect`, `architect/analyzer`. To remove
  this confound, pass explicit personas: `--agents opus:architect,sonnet:architect`.
