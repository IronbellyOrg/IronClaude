# Diagnosability Context Card
failing_component: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh (count_markers :206-212; step 5 :235-251)
3-W coverage: when=yes (exit code + token), where=partial (token + stderr path on failure; silent on false pass), why=partial
verdict: partial (both defects are silent false passes; directly observable by a hermetic real-git test: exit code, commit created or not)
issue_complexity: trivial (one file, two verified, localized predicates)
discriminator-required: no (observation-kind: trace; no categorical producer menu)
hard_stop: false
