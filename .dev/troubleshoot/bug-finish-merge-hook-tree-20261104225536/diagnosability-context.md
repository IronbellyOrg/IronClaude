# Diagnosability Context Card
failing_component: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh steps 6-8 (:271-292)
3-W coverage: when=no (a hook-changed commit passes silently), where=no, why=partial (hook output replayed to stderr only)
verdict: partial (directly observable in a hermetic real-git test: compare HEAD^{tree} with the index tree recorded before the commit)
issue_complexity: trivial (one script, one comparison)
discriminator-required: no (observation-kind: trace; no categorical producer menu)
hard_stop: false
