```yaml
contract_version: 1.8.0
status: needs_human_decision          # return contract carries status: partial and needs_human_decision: true (non-empty grounding-gaps.yaml, one dropped citation)
mode: post
tier_reached: 2
confidence_calibrated: 0.76           # mean of the three blind-calibrated reviewer cards (0.70, 0.82, 0.76); Tier-1 card 0.83
citations_total: 177                  # 169 re-read by three evidence-validator agents + 8 references re-read by the orchestrator
citations_revalidated: 177
citations_dropped: 1
citations_inferred: 11
citation_budget_policy: full_reread   # elected over sampled (stricter than the >20 band requires); citations_dropped is therefore absolute
reachability_gate_ran: true           # step 5.6a (required capabilities, annotation-free); step 5.6 durable-sink gate advisory only
reachability_ledger_path: artifacts/reachability-ledger.yaml
reachability_requirements_scanned: 5
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: null
```

