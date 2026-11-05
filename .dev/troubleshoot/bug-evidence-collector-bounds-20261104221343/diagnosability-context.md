# Diagnosability Context Card
failing_component: src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh (bounded :74-88; --out check :147-152); refs/conflict-intent.md:19 and refs/conflict-mechanical.md:247 (evidence path on restart)
3-W coverage: when=partial (A2 prints nothing until the hung command returns; C1 fails immediately with a token), where=partial (out_not_empty names the raw --out; timeout names the command only on the `timeout` path), why=partial (the run-log records only sync_tier3, not the EVIDENCE_FAIL reason)
verdict: partial (both defects reproduce deterministically in a hermetic scratch repo: elapsed time and the EVIDENCE_FAIL token)
issue_complexity: trivial (one script function plus one path convention across two refs and one e2e test)
discriminator-required: no (observation-kind: trace; no categorical producer menu)
hard_stop: false
