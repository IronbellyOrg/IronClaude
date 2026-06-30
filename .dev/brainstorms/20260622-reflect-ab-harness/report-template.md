# Reflect Run Report — TEMPLATE (filled once per gate run, both methods)

> Every inference run AND every cli run fills this identical template so the scoring subagent
> can parse them uniformly. Save as `<run-dir>/run-report.md`. All values must be backed by the
> run's own `return-contract.yaml` / `REPORT.md` — no fabrication.

```yaml
run_id: <method>-<NN>            # e.g. inference-03, cli-05
method: inference | cli
sample_commit: <sha>             # HEAD of exp/reflect-ab the run audited
base_commit: <start_commit sha>  # the frozen audit base
timestamp: <ISO-8601>
output_dir: <abs path to this run's reflect output>

# --- G1 Fan-out evidence ---
tier_reached: 1 | 2
fanned_out: true | false         # true iff >=2 reviewer cards exist on disk
reviewer_card_count: <int>       # count of <out>/reviewer-cards/*.md (or reviewer-briefs/)
merge_method: adversarial | single-reviewer-fallback | none
degraded_to_fixture: true | false   # true if the run produced a verdict with NO real reviewer artifacts

# --- Audit output (the deviations this run reported) ---
deviations_found:
  - id: <free>            # the run's own label
    file: <path>
    line: <n|range>
    reported_class: authorized | necessary | drift | regression
    severity: low | med | high
    grounding: grounded | inferred
    citation_resolves: true | false   # re-read check: does file:line match the claim?
verdict_status: success | partial | failed
regression_present: true | false
promotion_would_fire: true | false   # would the 9-condition gate have promoted? (should be FALSE)

# --- Cost ---
tokens_total: <int|null>
wall_clock_ms: <int|null>
contract_path: <abs path to return-contract.yaml>
```

## Filling instructions

1. `reviewer_card_count` / `fanned_out`: list the run's output dir; count reviewer card/brief
   files. 0 cards + a verdict ⇒ `degraded_to_fixture: true`.
2. `deviations_found`: transcribe from the run's `deviation-register` / REPORT.md deviation
   table. One row per reported deviation. Do NOT add or drop rows.
3. `citation_resolves`: for each cited `file:line`, re-Read it and mark whether the cited content
   matches (±5 lines). This is the citation-accuracy input to G6.
4. `promotion_would_fire`: read the contract's `promotion_*` / `regression_present`; the planted
   regression means a correct run reports FALSE.
5. Leave a field `null` only if the run genuinely did not emit it; never guess.
