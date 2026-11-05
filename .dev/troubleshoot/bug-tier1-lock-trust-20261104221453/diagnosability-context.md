# Diagnosability Context Card
failing_component: src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md step 5 (:82-94), executed by the attended session; rule row conflicts.py:202-210
3-W coverage: when=no (a successful `uv lock` leaves no trace; nothing records that a backend ran), where=partial (the plan names `regen:uv.lock`), why=no (no record of the pyproject fields that cause execution)
verdict: partial (the execution is directly observable in a scratch project: the backend's import side effect, probe-lock-trust.out:5)
issue_complexity: trivial (one pure check plus one step 5 call, the halt-row text and the trust note)
discriminator-required: no (observation-kind: trace; no categorical producer menu)
hard_stop: false
